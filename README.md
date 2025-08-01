# Student Voice Tracking System in Online Meets

A real-time audio processing system that tracks student participation in classroom discussions using speaker diarization, voice embeddings, and speech-to-text transcription. Now with MongoDB backend and Docker support!

## Features

- 🎤 **Real-time Audio Recording**: Continuous 10-second audio chunks
- 🎭 **Speaker Diarization**: Identifies different speakers using pyannote.audio
- 🎵 **Voice Embeddings**: Extracts unique voice signatures for each speaker
- 👥 **Speaker Recognition**: Matches speakers to known teachers and students
- 📝 **Speech Transcription**: Converts speech to text using faster-whisper
- 🔍 **Roll Number Extraction**: Automatically extracts student roll numbers from speech using regex and transformers
- 🆔 **Unknown Speaker Registration**: Handles unknown speakers by transcribing, extracting roll numbers, and registering new students
- 🏆 **Participation Leaderboard**: Tracks and ranks student participation time
- 🔧 **Audio Preprocessing**: Noise reduction and speech enhancement for better transcription
- 🐳 **Docker Support**: Containerized application with MongoDB
- 📊 **MongoDB Backend**: Scalable NoSQL database for better performance

## System Architecture

```
Audio Recording → Speaker Diarization → Voice Embeddings → Speaker Matching → Transcription → Roll Number Extraction → MongoDB Update → Leaderboard
```

## Requirements

- Python 3.8+ (for local development)
- Docker and Docker Compose (for containerized deployment)
- Microphone access
- Internet connection (for model downloads)
- See `requirements.txt` for all Python dependencies

## Installation

### Option 1: Docker (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cyberinnovator/student_interaction_tracker.git
   cd student_interaction_tracker
   ```

2. **Run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

   This will:
   - Build the Python application container
   - Start MongoDB container
   - Connect the app to MongoDB
   - Run the application

3. **For background execution:**
   ```bash
   docker-compose up -d
   ```

4. **View logs:**
   ```bash
   docker-compose logs -f app
   ```

### Option 2: Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cyberinnovator/student_interaction_tracker.git
   cd student_interaction_tracker
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up MongoDB:**
   - Install MongoDB locally or use Docker
   - Set environment variables:
     ```bash
     export MONGO_URL="mongodb://localhost:27017/"
     export DB_NAME="studentdb"
     ```

5. **Set up Hugging Face token:**
   - Get your token from [Hugging Face](https://huggingface.co/settings/tokens)
   - Update the token in `diarization.py` if required

## Usage

### Docker Usage

1. **Start the system:**
   ```bash
   docker-compose up --build
   ```

2. **Stop the system:**
   ```bash
   docker-compose down
   ```

3. **Access MongoDB:**
   ```bash
   docker-compose exec db mongosh -u user -p password
   ```

### Local Usage

1. **Start the system:**
   ```bash
   python main.py
   ```

2. **Register teachers first** (optional):
   - The system will prompt you to add teacher voices
   - Teachers are used as reference for speaker identification

3. **System will automatically:**
   - Record 10-second audio chunks
   - Identify speakers using diarization
   - Match speakers to known students/teachers
   - Transcribe speech for new/unknown speakers
   - Extract roll numbers from speech (using regex and transformers)
   - Register new students if roll number is found
   - Update participation leaderboard

## File Structure

```
student_interaction_tracker/
├── main.py                 # Main application entry point
├── db.py                   # Database operations (MongoDB)
├── diarization.py          # Speaker diarization using pyannote.audio
├── embedding.py            # Voice embedding extraction and comparison
├── audio_processing.py     # Audio preprocessing for better transcription
├── unknown_speaker.py      # Unknown speaker processing and transcription
├── rollno_extractor.py     # Roll number extraction using regex and transformers
├── migrate_to_mongodb.py   # Migration script from SQLite to MongoDB
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore           # Docker ignore file
├── embeddings/             # Stored voice embeddings
└── README.md               # This file
```

## Configuration

### Environment Variables

- `MONGO_URL`: MongoDB connection string (default: `mongodb://localhost:27017/`)
- `DB_NAME`: Database name (default: `studentdb`)

### Audio Processing
- **Preprocessing**: Gentle noise reduction and speech enhancement
- **Transcription**: CPU-optimized faster-whisper with tiny model
- **Language**: English (configurable)

### Speaker Detection
- **Diarization**: pyannote.audio 3.1
- **Embeddings**: Resemblyzer voice encoder
- **Similarity Threshold**: 0.6 (configurable)

### Database
- **Storage**: MongoDB (NoSQL database)
- **Collections**: students, teachers
- **Data**: Roll numbers, embedding paths, participation time
- **Indexes**: Automatic indexing on roll_no and teacher_id for performance

## Data Migration

If you have existing data in SQLite, you can migrate it to MongoDB:

```bash
# Run the migration script
python migrate_to_mongodb.py
```

This will:
- Connect to your existing SQLite database
- Transfer all students and teachers to MongoDB
- Preserve embedding file paths and participation times

## How It Works

1. **Audio Recording**: Records 10-second chunks continuously
2. **Diarization**: Separates audio into speaker segments
3. **Embedding Extraction**: Creates voice signatures for each speaker
4. **Speaker Matching**: Compares embeddings with known speakers
5. **Transcription**: Converts speech to text for unknown speakers
6. **Roll Number Extraction**: Uses regex and transformers to find roll numbers
7. **MongoDB Update**: Saves new students and updates participation time
8. **Leaderboard**: Displays participation rankings

## Roll Number Patterns

The system recognizes these patterns in speech:
- "roll no. is 123"
- "roll number is 123"
- "role number is 123" (common transcription)
- "my roll no. is 123"
- "my role number is 123"
- "i am 123" (fallback)

## Troubleshooting

### Common Issues

1. **No speakers detected**: Check microphone permissions and audio levels
2. **Transcription errors**: Ensure clear speech and minimal background noise
3. **Roll number not extracted**: Speak clearly and use supported patterns
4. **Model download issues**: Check internet connection and Hugging Face token
5. **MongoDB connection issues**: Check if MongoDB container is running

### Docker Issues

1. **Container won't start**: Check Docker and Docker Compose installation
2. **MongoDB connection failed**: Ensure MongoDB container is healthy
3. **Permission issues**: Run with appropriate user permissions

### Performance Tips

- Use a quiet environment for better transcription
- Speak clearly when providing roll numbers
- Ensure stable internet for model downloads
- Close other audio applications
- Use Docker for consistent environment

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Acknowledgments

- [pyannote.audio](https://github.com/pyannote/pyannote-audio) for speaker diarization
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) for speech transcription
- [Resemblyzer](https://github.com/resemble-ai/Resemblyzer) for voice embeddings
- [librosa](https://librosa.org/) for audio processing 
- [transformers](https://github.com/huggingface/transformers) for roll number extraction
- [MongoDB](https://www.mongodb.com/) for the database backend
