from PIL import Image, ImageDraw

def draw_realistic_architecture():
    # 1. Create a large, high-res canvas (1000x700) with a dark theme
    img = Image.new("RGB", (1000, 700), color="#0B0F19")
    draw = ImageDraw.Draw(img)

    # Helper function to draw infrastructure nodes
    def draw_node(coords, label, bg_color, outline_color):
        draw.rounded_rectangle(coords, radius=6, fill=bg_color, outline=outline_color, width=2)
        lines = label.split('\n')
        y_offset = coords[1] + (coords[3]-coords[1])//2 - (len(lines)*10)
        for line in lines:
            draw.text((coords[0] + 15, y_offset), line, fill="#F8FAFC")
            y_offset += 20

    # 2. Draw Virtual Private Cloud (VPC) Boundary
    draw.rectangle([50, 50, 950, 650], outline="#475569", width=2)
    draw.text((60, 60), "Production VPC (CIDR: 10.0.0.0/16)", fill="#94A3B8")

    # 3. Draw Availability Zones
    draw.rectangle([70, 100, 490, 620], outline="#334155", width=1)
    draw.text((80, 110), "Availability Zone A (us-east-1a)", fill="#64748B")
    
    draw.rectangle([510, 100, 930, 620], outline="#334155", width=1)
    draw.text((520, 110), "Availability Zone B (us-east-1b)", fill="#64748B")

    # 4. Draw Subnets (Public, Compute, Database)
    draw.rectangle([90, 140, 910, 260], outline="#38BDF8", width=1)
    draw.text((100, 150), "Public Subnet (DMZ / Ingress Tier)", fill="#38BDF8")

    draw.rectangle([90, 280, 910, 440], outline="#818CF8", width=1)
    draw.text((100, 290), "Private Subnet (Application / Compute Tier)", fill="#818CF8")

    draw.rectangle([90, 460, 910, 600], outline="#34D399", width=1)
    draw.text((100, 470), "Private Subnet (Database / Caching Tier)", fill="#34D399")

    # 5. Populate Nodes (Ingress Layer)
    draw_node([150, 180, 300, 240], "AWS WAF\n(Web App Firewall)", "#1E293B", "#38BDF8")
    draw_node([400, 180, 600, 240], "Application Load Balancer\n(Active-Active Routing)", "#1E293B", "#38BDF8")
    draw_node([700, 180, 850, 240], "NAT Gateway\n(Outbound Traffic)", "#1E293B", "#38BDF8")

    # 6. Populate Nodes (Compute Layer)
    draw_node([120, 320, 270, 380], "EKS Worker Node\n(Microservice Pod A)", "#1E293B", "#818CF8")
    draw_node([300, 320, 450, 380], "EKS Worker Node\n(Microservice Pod B)", "#1E293B", "#818CF8")
    draw_node([550, 320, 700, 380], "EKS Worker Node\n(Microservice Pod C)", "#1E293B", "#818CF8")
    draw_node([730, 320, 880, 380], "EKS Worker Node\n(Microservice Pod D)", "#1E293B", "#818CF8")

    # 7. Populate Nodes (Data Layer)
    draw_node([150, 500, 350, 570], "Amazon Aurora RDS\n(Primary Master DB)", "#1E293B", "#34D399")
    draw_node([400, 500, 600, 570], "ElastiCache Cluster\n(Redis Session Store)", "#1E293B", "#34D399")
    draw_node([650, 500, 850, 570], "Amazon Aurora RDS\n(Read Replica DB)", "#1E293B", "#34D399")

    # 8. Draw Network Traffic Flow Lines
    def draw_line(p1, p2):
        draw.line([p1, p2], fill="#94A3B8", width=2)

    # WAF to Load Balancer
    draw_line((300, 210), (400, 210))
    # Load Balancer down to EKS Nodes
    draw_line((500, 240), (195, 320))
    draw_line((500, 240), (375, 320))
    draw_line((500, 240), (625, 320))
    draw_line((500, 240), (805, 320))
    
    # EKS Nodes down to Databases & Cache
    draw_line((375, 380), (250, 500)) # Pod B to Master DB
    draw_line((375, 380), (500, 500)) # Pod B to Redis Cache
    draw_line((625, 380), (500, 500)) # Pod C to Redis Cache
    draw_line((625, 380), (750, 500)) # Pod C to Replica DB

    # DB Asynchronous Replication Line
    draw.line([(350, 535), (650, 535)], fill="#34D399", width=2)
    draw.text((390, 515), "<-- Async Data Replication -->", fill="#34D399")

    img.save("enterprise_architecture_diagram.png")
    print("Saved high-density realistic image: enterprise_architecture_diagram.png")

if __name__ == "__main__":
    draw_realistic_architecture()