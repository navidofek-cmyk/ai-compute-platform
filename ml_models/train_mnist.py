"""
MNIST Model Training and ONNX Export
Trains a simple feedforward neural network on MNIST dataset and exports to ONNX format
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import os

class MNISTNet(nn.Module):
    """Simple feedforward neural network for MNIST digit classification"""
    
    def __init__(self):
        super(MNISTNet, self).__init__()
        self.fc1 = nn.Linear(784, 128)
        self.relu1 = nn.ReLU()
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.fc3 = nn.Linear(64, 10)
        
    def forward(self, x):
        x = x.view(-1, 784)  # Flatten 28x28 to 784
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

def train_model(epochs=5, batch_size=64, learning_rate=0.001):
    """Train the MNIST model"""
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Data transformations
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.1307,), (0.3081,))
    ])
    
    # Load MNIST dataset
    print("Loading MNIST dataset...")
    train_dataset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    test_dataset = datasets.MNIST(root='./data', train=False, download=True, transform=transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
    
    # Initialize model
    model = MNISTNet().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Training loop
    print(f"\nTraining for {epochs} epochs...")
    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            # Backward pass and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            # Statistics
            running_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            
            if (batch_idx + 1) % 200 == 0:
                print(f'Epoch [{epoch+1}/{epochs}], Step [{batch_idx+1}/{len(train_loader)}], '
                      f'Loss: {running_loss/200:.4f}, Accuracy: {100*correct/total:.2f}%')
                running_loss = 0.0
        
        # Test accuracy
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for images, labels in test_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        
        test_accuracy = 100 * correct / total
        print(f'Epoch [{epoch+1}/{epochs}] Test Accuracy: {test_accuracy:.2f}%\n')
    
    return model

def export_to_onnx(model, output_path='mnist_model.onnx'):
    """Export trained model to ONNX format"""
    
    model.eval()
    
    # Create dummy input (batch_size=1, 1 channel, 28x28 image)
    dummy_input = torch.randn(1, 1, 28, 28)
    
    # Export to ONNX
    print(f"\nExporting model to {output_path}...")
    torch.onnx.export(
        model,
        dummy_input,
        output_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={
            'input': {0: 'batch_size'},
            'output': {0: 'batch_size'}
        }
    )
    
    print(f"Model exported successfully to {output_path}")
    print(f"Model size: {os.path.getsize(output_path) / 1024:.2f} KB")

def main():
    """Main training and export pipeline"""
    
    print("="*60)
    print("MNIST Model Training and ONNX Export")
    print("="*60)
    
    # Train model
    model = train_model(epochs=5, batch_size=64, learning_rate=0.001)
    
    # Save PyTorch model
    torch.save(model.state_dict(), 'mnist_model.pth')
    print("\nPyTorch model saved to mnist_model.pth")
    
    # Export to ONNX
    export_to_onnx(model, 'mnist_model.onnx')
    
    print("\n" + "="*60)
    print("Training and export completed successfully!")
    print("="*60)
    print("\nYou can now use mnist_model.onnx with ONNX Runtime in C++")

if __name__ == '__main__':
    main()
