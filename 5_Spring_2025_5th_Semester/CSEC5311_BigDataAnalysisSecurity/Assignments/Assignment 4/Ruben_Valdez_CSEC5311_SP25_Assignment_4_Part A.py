#Ruben_Valdez_CSEC5311_SP25_Assignment_4_Part A.py
# Import necessary libraries
import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import matplotlib.pyplot as plt
import numpy as np


"""
Dataset Reference:
Hojjat, K. (2023). MNIST dataset. Kaggle. Retrieved from
https://www.kaggle.com/datasets/hojjatk/mnist-dataset
"""

# Define Variational Autoencoder (VAE) model
class VAE(nn.Module):
    """
    Variational Autoencoder (VAE) model for the MNIST dataset.
    The VAE consists of an encoder, a latent space representation, and a decoder.

    Attributes:
        encoder (nn.Sequential): Neural network for encoding input images.
        fc_mu (nn.Linear): Fully connected layer for mean of latent distribution.
        fc_logvar (nn.Linear): Fully connected layer for log-variance of latent distribution.
        decoder_fc (nn.Linear): Fully connected layer mapping latent space to decoder input.
        decoder (nn.Sequential): Neural network for decoding latent vectors to images.
    """
    def __init__(self, latent_dim=2):
        """
        Initializes the VAE model with the given latent space dimension.

        Args:
            latent_dim (int): Dimension of the latent space.
        """
        super(VAE, self).__init__()

        # Encoder network
        self.encoder = nn.Sequential(
            nn.Flatten(),                # Flatten input (28x28) into a 1D vector
            nn.Linear(28 * 28, 400),      # Fully connected layer with 400 neurons
            nn.ReLU()
        )

        # Latent space parameters
        self.fc_mu = nn.Linear(400, latent_dim)       # Mean of latent space
        self.fc_logvar = nn.Linear(400, latent_dim)   # Log variance of latent space

        # Decoder network
        self.decoder_fc = nn.Linear(latent_dim, 400)
        self.decoder = nn.Sequential(
            nn.ReLU(),
            nn.Linear(400, 28 * 28),
            nn.Sigmoid()   # Sigmoid to ensure pixel values are between 0 and 1
        )

    def reparameterize(self, mu, logvar):
        """
        Performs the reparameterization trick to sample from a Gaussian distribution.
        Ensures that the model learns a continuous and differentiable latent space.

        Args:
            mu (torch.Tensor): Mean of the latent space.
            logvar (torch.Tensor): Log variance of the latent space.

        Returns:
            torch.Tensor: Sampled latent vector.
        """
        std = torch.exp(0.5 * logvar)  # Convert log variance to standard deviation
        eps = torch.randn_like(std)    # Random normal noise
        return mu + eps * std          # Sampled latent vector

    def forward(self, x):
        """
        Forward pass through the VAE model.

        Args:
            x (torch.Tensor): Input image tensor.

        Returns:
            tuple: Reconstructed image, mean, and log variance.
        """
        encoded = self.encoder(x)
        mu = self.fc_mu(encoded)
        logvar = self.fc_logvar(encoded)
        z = self.reparameterize(mu, logvar)

        decoded = self.decoder_fc(z)
        decoded = self.decoder(decoded)

        return decoded, mu, logvar


def loss_function(recon_x, x, mu, logvar):
    """
    Computes the loss function for VAE training.

    The loss consists of:
    - Reconstruction Loss (Binary Cross-Entropy) which ensures output similarity to input.
    - KL Divergence Loss (KLD) which regularizes the latent space.

    Args:
        recon_x (torch.Tensor): Reconstructed image.
        x (torch.Tensor): Original image.
        mu (torch.Tensor): Mean of the latent space.
        logvar (torch.Tensor): Log variance of the latent space.

    Returns:
        torch.Tensor: Total loss (Reconstruction Loss + KL Divergence).
    """
    BCE = nn.functional.binary_cross_entropy(recon_x, x.view(-1, 28 * 28), reduction='sum')
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())  # KL divergence loss
    return BCE + KLD


def load_data():
    """
    Loads the MNIST dataset and applies transformations.

    Returns:
        DataLoader: Dataloader object for training set.
    """
    transform = transforms.Compose([transforms.ToTensor()])
    train_dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    return data.DataLoader(train_dataset, batch_size=64, shuffle=True)


def train(vae, train_loader, optimizer, device, num_epochs=10):
    """
    Trains the VAE model using the MNIST dataset.

    Args:
        vae (VAE): The Variational Autoencoder model.
        train_loader (DataLoader): The training dataset loader.
        optimizer (torch.optim.Optimizer): The optimizer for training.
        device (torch.device): The device to run the training on (CPU/GPU).
        num_epochs (int): Number of epochs to train the model.
    """
    for epoch in range(num_epochs):
        vae.train()
        train_loss = 0
        for batch, (imgs, _) in enumerate(train_loader):
            imgs = imgs.to(device).view(-1, 28 * 28)
            optimizer.zero_grad()
            recon_imgs, mu, logvar = vae(imgs)
            loss = loss_function(recon_imgs, imgs, mu, logvar)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        print(f'Epoch {epoch+1}, Loss: {train_loss / len(train_loader.dataset):.4f}')


def main():
    """
    Main function to execute the full VAE training, image reconstruction, 
    sample generation, and latent space visualization.
    """
    # Initialize device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load dataset
    train_loader = load_data()

    # Initialize model and optimizer
    vae = VAE().to(device)
    optimizer = optim.Adam(vae.parameters(), lr=1e-3)

    # Train the model
    train(vae, train_loader, optimizer, device)

    # Reconstruct and visualize images
    vae.eval()
    data_iter = iter(train_loader)
    imgs, _ = next(data_iter)
    imgs = imgs.to(device).view(-1, 28 * 28)

    with torch.no_grad():
        recon_imgs, _, _ = vae(imgs)

    imgs, recon_imgs = imgs.cpu().numpy(), recon_imgs.cpu().numpy()

    fig, axes = plt.subplots(2, 10, figsize=(10, 2))
    for i in range(10):
        axes[0, i].imshow(imgs[i].reshape(28, 28), cmap='gray')
        axes[1, i].imshow(recon_imgs[i].reshape(28, 28), cmap='gray')
        axes[0, i].axis('off')
        axes[1, i].axis('off')
    plt.show()

    # Generate new samples
    with torch.no_grad():
        z = torch.randn(10, 2).to(device)
        samples = vae.decoder(vae.decoder_fc(z)).cpu().numpy()

    fig, axes = plt.subplots(1, 10, figsize=(10, 2))
    for i in range(10):
        axes[i].imshow(samples[i].reshape(28, 28), cmap='gray')
        axes[i].axis('off')
    plt.show()

    # Visualize latent space
    z_points, labels = [], []
    for imgs, lbls in train_loader:
        imgs = imgs.to(device).view(-1, 28 * 28)
        with torch.no_grad():
            _, mu, _ = vae(imgs)
        z_points.append(mu.cpu().numpy())
        labels.append(lbls.numpy())

    z_points = np.concatenate(z_points, axis=0)
    labels = np.concatenate(labels, axis=0)

    plt.figure(figsize=(8, 6))
    plt.scatter(z_points[:, 0], z_points[:, 1], c=labels, cmap='jet', alpha=0.5)
    plt.colorbar()
    plt.xlabel("Latent Dimension 1")
    plt.ylabel("Latent Dimension 2")
    plt.title("Latent Space Visualization")
    plt.show()

    print(f"\nEnd of Program\n")


# Run main function
if __name__ == "__main__":
    main()
