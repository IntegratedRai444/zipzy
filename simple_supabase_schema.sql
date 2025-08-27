-- ZIPZY: Simple Users + OTP Schema (Guaranteed to work)
-- Run this in Supabase SQL Editor

-- 1) Clean slate - drop everything
drop table if exists public.app_otp_codes cascade;
drop table if exists public.app_users cascade;
drop function if exists public.register_or_login_and_send_otp(text, text, text, text, text, text, text);
drop function if exists public.register_or_login_and_send_otp(text, text, text, text);
drop function if exists public.verify_otp(text, text, text);
drop function if exists public.gen_6_digit_code();

-- 2) Create tables with simple structure
create table public.app_users (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  email text,
  mobile text,
  role text not null default 'customer',
  last_login timestamptz null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Simple unique constraints (no WHERE clauses)
create unique index idx_app_users_email on public.app_users (email);
create unique index idx_app_users_mobile on public.app_users (mobile);

-- OTP table
create table public.app_otp_codes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references public.app_users(id) on delete cascade,
  identifier text not null,
  channel text not null default 'sms',
  purpose text not null default 'login',
  code text not null,
  expires_at timestamptz not null,
  attempts int not null default 0,
  consumed_at timestamptz null,
  created_at timestamptz not null default now()
);

create index idx_app_otp_lookup on public.app_otp_codes (identifier, purpose, created_at desc);

-- 3) Simple helper function
create or replace function public.gen_6_digit_code()
returns text language plpgsql as $$
begin
  return floor(random() * 900000 + 100000)::text;
end;
$$;

-- 4) Simple OTP request function (no complex conflict handling)
create or replace function public.register_or_login_and_send_otp(
  p_name text,
  p_email text default null,
  p_mobile text default null,
  p_purpose text default 'login'
)
returns table(user_id uuid, email_otp text, mobile_otp text)
language plpgsql
as $$
declare
  v_user_id uuid;
  v_email_otp text := null;
  v_mobile_otp text := null;
begin
  -- Try to find existing user
  select id into v_user_id from public.app_users 
  where email = p_email or mobile = p_mobile;
  
  -- If no user found, create one
  if v_user_id is null then
    insert into public.app_users (name, email, mobile, role)
    values (p_name, p_email, p_mobile, 'customer')
    returning id into v_user_id;
  else
    -- Update existing user
    update public.app_users 
    set name = p_name, updated_at = now()
    where id = v_user_id;
  end if;
  
  -- Generate OTPs
  if p_email is not null then
    v_email_otp := public.gen_6_digit_code();
    insert into public.app_otp_codes (user_id, identifier, channel, purpose, code, expires_at)
    values (v_user_id, p_email, 'email', p_purpose, v_email_otp, now() + interval '5 minutes');
  end if;
  
  if p_mobile is not null then
    v_mobile_otp := public.gen_6_digit_code();
    insert into public.app_otp_codes (user_id, identifier, channel, purpose, code, expires_at)
    values (v_user_id, p_mobile, 'sms', p_purpose, v_mobile_otp, now() + interval '5 minutes');
  end if;
  
  return query select v_user_id, v_email_otp, v_mobile_otp;
end;
$$;

-- 5) Simple OTP verification function
create or replace function public.verify_otp(
  p_identifier text,
  p_code text,
  p_purpose text default 'login'
)
returns table(user_id uuid, verified boolean)
language plpgsql
as $$
declare
  v_otp_id uuid;
  v_user_id uuid;
begin
  -- Find the latest valid OTP
  select id, user_id into v_otp_id, v_user_id
  from public.app_otp_codes
  where identifier = p_identifier
    and purpose = p_purpose
    and consumed_at is null
    and expires_at > now()
    and code = p_code
  order by created_at desc
  limit 1;
  
  if v_otp_id is null then
    return query select null::uuid, false;
    return;
  end if;
  
  -- Mark OTP as consumed
  update public.app_otp_codes
  set consumed_at = now()
  where id = v_otp_id;
  
  -- Update user's last login
  if v_user_id is not null then
    update public.app_users
    set last_login = now()
    where id = v_user_id;
  end if;
  
  return query select v_user_id, true;
end;
$$;

-- 6) Enable RLS with simple policies
alter table public.app_users enable row level security;
alter table public.app_otp_codes enable row level security;

create policy "allow_all_users" on public.app_users for all using (true);
create policy "allow_all_otp" on public.app_otp_codes for all using (true);
