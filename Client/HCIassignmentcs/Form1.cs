using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Net;
using System.Net.Sockets;


namespace HCIassignmentcs
{
    public partial class Form1 : Form
    {
        private PictureBox ballPictureBox;
        private Timer timer;
        private Socket clientSocket;
        


        public Form1()
        {
            InitializeComponent();
            clientSocket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            clientSocket.Connect(new IPEndPoint(IPAddress.Parse("127.0.0.1"), 8080));
            Console.WriteLine("Connection Made ! with " + "localhost");
            // Create the ball PictureBox control
            ballPictureBox = new PictureBox();
            ballPictureBox.BackColor = Color.Transparent;
            ballPictureBox.BackgroundImage = Properties.Resources.ball;
            ballPictureBox.BackgroundImageLayout = ImageLayout.Stretch;
            ballPictureBox.Size = new Size(50, 50);
            ballPictureBox.Location = new Point(0, 0);
            Controls.Add(ballPictureBox);
           
            // Create the timer control
            timer = new Timer();
            timer.Interval = 1;
            timer.Tick += Timer_Tick;
            timer.Start();

      
        }

        private void Timer_Tick(object sender, EventArgs e)
        {
            byte[] buffer = new byte[1024];
            int bytesReceived = clientSocket.Receive(buffer);
            string data = Encoding.ASCII.GetString(buffer, 0, bytesReceived);
            string[] points = data.Split(',');
            if (points.Length >= 21)
            {
                float x = float.Parse(points[0]);
                float y = float.Parse(points[1]);
                ballPictureBox.Location = new Point((int)x, (int)y);
            }


        }
    }
}
