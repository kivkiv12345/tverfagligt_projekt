### This Dockerfile is copied from:
### https://github.com/TotallyNotRust/Chivalry-2-Competitive-Platform/blob/main/Dockerfile

# Use the official Flutter Docker image as the base image
FROM ghcr.io/cirruslabs/flutter:latest

# Set the working directory in the container
WORKDIR /app

# Copy the entire project to the container
COPY . .

RUN flutter pub global activate dhttpd 
RUN flutter pub get
RUN flutter build web

EXPOSE 8080

CMD ["flutter", "pub", "global", "run", "dhttpd", "--path", "build/web/", "--host", "0.0.0.0"]
