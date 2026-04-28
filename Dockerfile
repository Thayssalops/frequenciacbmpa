# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# --- INÍCIO DAS ALTERAÇÕES ---
# 1. Atualiza o apt e instala o pacote 'locales' necessário para gerar novos idiomas.
# 2. Limpa o cache do apt para manter a imagem leve.
RUN apt-get update && \
    apt-get install -y locales && \
    rm -rf /var/lib/apt/lists/*

# 3. Descomenta a linha do pt_BR no arquivo locale.gen e gera o locale.
RUN sed -i -e 's/# pt_BR.UTF-8 UTF-8/pt_BR.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen

# 4. Define as variáveis de ambiente para forçar o uso do Português do Brasil.
ENV LANG pt_BR.UTF-8
ENV LC_ALL pt_BR.UTF-8
# --- FIM DAS ALTERAÇÕES ---

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code from the host to the container at /app
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]