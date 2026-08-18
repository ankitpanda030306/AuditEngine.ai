import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import io

class DiagramVisionInspector:
    def __init__(self):
        # Topology classes representing system architecture styles
        self.classes = [
            "Microservices Mesh Topology",
            "Monolithic / High-Load Ingress",
            "Distributed Database Cluster",
            "Public Cloud / Serverless Edge"
        ]
        
        # Determine compute device (GPU if available, else CPU)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Standard PyTorch vision transformation pipeline (Phase 2 Skill)
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406], 
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        self.model = self._initialize_model()

    def _initialize_model(self):
        # Using a lightweight, production-ready MobileNetV3 backbone
        weights = models.MobileNet_V3_Small_Weights.DEFAULT
        model = models.mobilenet_v3_small(weights=weights)
        
        # Modify final classification head for custom topology domains
        in_features = model.classifier[3].in_features
        model.classifier[3] = nn.Linear(in_features, len(self.classes))
        
        model.to(self.device)
        model.eval()
        return model

    def inspect_diagram(self, image_input) -> dict:
        """
        Accepts either a PIL Image object or a file path string.
        """
        if isinstance(image_input, str):
            image = Image.open(image_input).convert("RGB")
        elif isinstance(image_input, bytes):
            image = Image.open(io.BytesIO(image_input)).convert("RGB")
        else:
            image = image_input.convert("RGB")
            
        # Apply transformation and add batch dimension (1, C, H, W)
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(tensor)
            probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
            
            top_prob, top_idx = torch.max(probabilities, 0)
            
        detected_topology = self.classes[top_idx.item()]
        confidence = round(float(top_prob.item()) * 100, 2)
        
        # Security vulnerability inspection heuristic based on topology
        security_note = (
            "Review Ingress firewall rules and DDoS throttling." 
            if "Ingress" in detected_topology 
            else "Ensure multi-region replication and encrypted VPC peering."
        )
        
        return {
            "detected_topology": detected_topology,
            "confidence_pct": confidence,
            "security_recommendation": security_note
        }

if __name__ == "__main__":
    inspector = DiagramVisionInspector()
    
    # Create a synthetic image for local test verification
    test_img = Image.new("RGB", (300, 300), color=(73, 109, 137))
    result = inspector.inspect_diagram(test_img)
    
    print("=== PyTorch Vision Inspector Output ===")
    print(result)