using System;
using System.Diagnostics;
using System.Windows;

namespace UnplugReminder
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        // Triggered when the user clicks the primary "Shut Down" button
        private void Shutdown_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Set up the shutdown command. 
                // /s tells Windows to shut down
                // /t 0 tells Windows to do it immediately (0 seconds)
                ProcessStartInfo shutdownInfo = new ProcessStartInfo("shutdown", "/s /t 0")
                {
                    CreateNoWindow = true,
                    UseShellExecute = false
                };

                // Execute the system shutdown
                Process.Start(shutdownInfo);
                
                // Close our reminder app gracefully
                Application.Current.Shutdown();
            }
            catch (Exception ex)
            {
                // Solid error handling: if the OS denies the request or fails, let the user know cleanly.
                MessageBox.Show($"Could not initiate shutdown. System returned: \n{ex.Message}", 
                                "Shutdown Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        // Triggered when the user decides they don't want to shut down yet
        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            // Just close the app and return to Windows
            Application.Current.Shutdown();
        }
    }
}