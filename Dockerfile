# Step 1: Build the React application
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Step 2: Serve the application using Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80 for Hugging Face Spaces
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]
