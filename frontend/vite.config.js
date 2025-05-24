// Import the defineConfig function from Vite
import { defineConfig } from 'vite';
// Import the React plugin for Vite
import react from '@vitejs/plugin-react';

// Export the Vite configuration
export default defineConfig({
  // Specify the plugins to use
  plugins: [react()], // Enables React support in Vite
});

