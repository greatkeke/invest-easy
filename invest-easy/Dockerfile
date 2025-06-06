# Stage 1: Build the Angular application
FROM node:18-alpine AS build

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy all files
COPY . .

# Build both client and server
RUN npm run build

# Stage 2: Serve the application
FROM node:18-alpine

WORKDIR /app

# Copy built files from build stage
COPY --from=build /app/dist/invest-easy/browser ./dist/invest-easy/browser
COPY --from=build /app/dist/invest-easy/server ./dist/invest-easy/server

# Install production dependencies
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

# Expose port
EXPOSE 4000

VOLUME /app/dist/invest-easy/browser/assets 

# Start the SSR server
CMD ["npm", "run", "serve:ssr:invest-easy"]
