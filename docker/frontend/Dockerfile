FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Expose port
EXPOSE 5173

# Run development server with host binding
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
