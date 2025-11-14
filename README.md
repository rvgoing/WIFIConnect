# Flask Static IP Test on Render

A simple Flask web application designed to test and verify static IP functionality on Render.

## Features

- Displays server's public IP address
- Shows server's local IP and hostname
- Displays client's IP address
- Health check endpoint for monitoring
- Clean, modern UI with real-time information

## Local Testing

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Visit `http://localhost:5000` in your browser

## Deployment on Render

### Option 1: Using render.yaml (Recommended)

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" and select "Blueprint"
4. Connect your GitHub repository
5. Render will automatically detect the `render.yaml` file and configure the service

### Option 2: Manual Deployment

1. Push this repository to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com/)
3. Click "New" and select "Web Service"
4. Connect your GitHub repository
5. Configure the service:
   - **Name**: wificonnect-static-ip-test
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Health Check Path**: `/health`

### Enabling Static IP on Render

1. After deployment, go to your service settings
2. Navigate to the "Network" or "Outbound IP" section
3. Enable "Static Outbound IP" (this may require a paid plan)
4. Note the static IP address provided by Render
5. Visit your deployed application URL to verify the public IP matches the static IP

## Testing Static IP

Once deployed with a static IP:

1. Visit your application URL (e.g., `https://your-app.onrender.com`)
2. Check the "Server Public IP" displayed on the page
3. This should match the static IP provided in Render's settings
4. You can refresh the page multiple times to confirm the IP remains constant
5. Use the `/health` endpoint for monitoring: `https://your-app.onrender.com/health`

## Verifying Static IP Externally

You can verify the static IP by making requests from external services:

```bash
# Using curl
curl https://your-app.onrender.com/

# Check multiple times to ensure consistency
for i in {1..5}; do curl -s https://your-app.onrender.com/ | grep "Server Public IP"; done
```

## Files Structure

```
.
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # HTML template with IP information display
├── requirements.txt       # Python dependencies
├── render.yaml           # Render deployment configuration
├── Procfile              # Alternative deployment configuration
└── README.md             # This file
```

## Endpoints

- `/` - Main page displaying IP information
- `/health` - Health check endpoint (returns JSON status)

## Notes

- Static IP on Render typically requires a paid plan
- The public IP shown is the outbound IP address of the server
- The application uses the `ipify.org` API to determine the public IP
- The client IP will show your IP address (or proxy IP if behind one)

## Troubleshooting

If the public IP shows "Unable to determine":
- Check if the server has internet connectivity
- Verify that outbound requests are allowed
- Check Render logs for any errors

If the static IP doesn't match:
- Ensure the static IP feature is enabled in Render settings
- Wait a few minutes after enabling for changes to propagate
- Check if you're on a plan that supports static IPs
