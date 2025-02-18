# Wits Planetary Health Research Global Partners Dashboard

An interactive visualization of global research partnerships for the Wits Planetary Health Research division.

## Features

- Interactive world map showing research partner locations
- Filter partners by project (CHAMNHA, HE2AT, HIGH, ENBEL)
- Hover information showing institution details
- Partnership statistics
- Responsive design for desktop and mobile viewing

## Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/wits-phr-partners.git
cd wits-phr-partners
```

2. The dashboard is static HTML/JavaScript and can be deployed directly to GitHub Pages:
   - Go to your repository settings
   - Navigate to "Pages"
   - Select "main" branch and "/root" folder
   - Click "Save"

Your dashboard will be available at: https://yourusername.github.io/wits-phr-partners/

## Local Development

To run locally, you can use any static file server. For example, with Python:

```bash
python -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Technologies Used

- Plotly.js for map visualization
- HTML5/CSS3 for layout and styling
- Vanilla JavaScript for interactivity

## License

MIT License
