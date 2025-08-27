const { createClient } = require('@supabase/supabase-js');
const bcrypt = require('bcryptjs');

const supabaseUrl = 'https://virwqwhvwpiayaabcnqe.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZpcndxd2h2d3BpYXlhYWJjbnFlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU4OTAxOTEsImV4cCI6MjA3MTQ2NjE5MX0.IY9t4aYZq-uJSFFMsAyVmcLeY8MJlzHqkS4GJG4RAt4';

const supabase = createClient(supabaseUrl, supabaseKey);

async function setupAdminUser() {
  try {
    console.log('Setting up admin user...');

    // Check if admin user already exists
    const { data: existingAdmin, error: checkError } = await supabase
      .from('users')
      .select('id')
      .eq('email', 'admin@zipzy.com')
      .single();

    if (existingAdmin) {
      console.log('Admin user already exists!');
      return;
    }

    // Hash password
    const hashedPassword = await bcrypt.hash('admin123', 12);

    // Create admin user
    const { data: adminUser, error: insertError } = await supabase
      .from('users')
      .insert([
        {
          full_name: 'Admin User',
          email: 'admin@zipzy.com',
          password: hashedPassword,
          role: 'admin'
        }
      ])
      .select('id, full_name, email, role')
      .single();

    if (insertError) {
      console.error('Error creating admin user:', insertError);
      return;
    }

    console.log('Admin user created successfully!');
    console.log('Email: admin@zipzy.com');
    console.log('Password: admin123');
    console.log('Role:', adminUser.role);
    console.log('Name:', adminUser.full_name);

  } catch (error) {
    console.error('Setup error:', error);
  }
}

setupAdminUser();
