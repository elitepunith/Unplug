using System;
using System.Diagnostics;
using System.Windows;

namespace Unplug
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }

        private void Shutdown_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                ProcessStartInfo shutdownInfo = new ProcessStartInfo("shutdown", "/s /t 0")
                {
                    CreateNoWindow = true,
                    UseShellExecute = false
                };

                Process.Start(shutdownInfo);
                Application.Current.Shutdown();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Could not initiate shutdown. System returned: \n{ex.Message}", 
                                "Shutdown Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            Application.Current.Shutdown();
        }
    }
}