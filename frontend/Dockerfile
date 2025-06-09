# Use Node.js base image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app
COPY . .

# Expose default Nuxt dev port
EXPOSE 3000

# Default command to run Nuxt in dev mode
CMD ["npm", "run", "dev"]
