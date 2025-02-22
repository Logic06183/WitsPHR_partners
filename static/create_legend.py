from PIL import Image, ImageDraw, ImageFont
import os

def create_map_legend():
    # Create a new image with white background and transparency
    width = 200
    height = 280
    image = Image.new('RGBA', (width, height), (255, 255, 255, 240))
    draw = ImageDraw.Draw(image)

    # Define colors and projects
    colors = {
        'CHAMNHA': '#2E86C1',
        'HE²AT': '#28B463',
        'HIGH': '#E67E22',
        'ENBEL': '#C0392B'
    }

    # Draw title
    draw.text((10, 10), "Research Projects", fill='black')

    # Draw project markers
    y = 40
    for project, color in colors.items():
        # Draw circle
        draw.ellipse([10, y, 20, y+10], fill=color, outline=color)
        # Draw text
        draw.text((30, y-2), project, fill='black')
        y += 30

    # Draw HE²AT Study Sites
    y += 10
    draw.rectangle([10, y, 30, y+20], fill='#FFA726', outline='#666666')
    draw.text((40, y+2), "HE²AT Study Sites", fill='black')

    # Save the image
    image.save('map_legend.png', 'PNG')
    print("Legend has been created as 'map_legend.png'")

if __name__ == "__main__":
    create_map_legend()