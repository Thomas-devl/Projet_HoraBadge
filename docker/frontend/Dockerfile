FROM node:18-alpine

# Set work directory
WORKDIR /app

# Copy package files
COPY ../../frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY ../../frontend ./

# Expose port
EXPOSE 5173

# Run development server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
