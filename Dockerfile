# Use the latest Arch Linux image as the base
FROM archlinux:latest

# Update system repositories and upgrade packages
RUN pacman -Syu --noconfirm

# Install base-devel and git (dependencies for pikaur and AUR packages)
RUN pacman -S --noconfirm base-devel git python-setuptools

# Add a non-root user to run yay
RUN useradd -m user && \
    echo "user ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/user

# Set user for yay
USER user
WORKDIR /home/user

# Install yay
RUN git clone https://aur.archlinux.org/yay.git && \
    cd yay && \
    makepkg -si --noconfirm

# Use pikaur to install python-playwright from AUR
RUN yay -S --noconfirm python-pytelegrambotapi
RUN yay -S --noconfirm python-playwright



# Switch back to the root user if needed for further operations
USER root
RUN playwright install

RUN pacman -S --noconfirm \
    nss \
    nspr \
    atk \
    at-spi2-atk \
    cups \
    libdrm \
    libxkbcommon \
    libxcomposite \
    libxdamage \
    libxext \
    libxfixes \
    libxrandr \
    mesa \
    pango \
    cairo \
    alsa-lib

# Copy the contents of the local script directory to /script inside the container
COPY ./script /script

# Set the working directory to /script
WORKDIR /script

# By default, run a shell. You could also specify your script here.
CMD ["python3", "bot.py"]
