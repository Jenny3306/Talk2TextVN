# Talk2TextVN – Offline Vietnamese Speech-to-Text

## 🎯 Product Goal

**Talk2TextVN** is an offline speech-to-text application that is designed in combination with Gemma 3n to help three main user groups:
- **Older Adults**: Individuals who have difficulty typing and would benefit from a voice-to-text solution.
- **People with Hearing Impairments**: Offering real-time transcription of spoken words.
- **Users Unfamiliar with Typing**: Providing an easy-to-use, hands-free alternative to typing.

This application converts spoken Vietnamese into text without the need for an internet connection, ensuring privacy and accessibility for all users. Its aim is to provide a tool for real-world accessibility challenges, ensuring that users, regardless of their typing proficiency, can communicate efficiently and privately.

## 📜 About Gemma 3n

**Gemma 3n** is Google's cutting-edge multimodal AI model, optimized for on-device applications. It supports real-time processing of audio, text, and images, making it ideal for offline applications like **Talk2TextVN**. 

By integrating **Gemma 3n**, this project is able to:
- Leverage its **on-device performance** for fast, efficient processing.
- Ensure **privacy-first** functionality by running fully offline without the need for internet.
- Benefit from **multilingual capabilities**, making the system more adaptable across various contexts.

Using **Gemma 3n**, we can provide highly accurate Vietnamese speech-to-text conversion while maintaining full control over user data and ensuring the system operates smoothly without any online dependency.

## 📝 Key Features

- **Offline Operation**: Fully functional without the need for internet access. 
- **Speech Recognition**: Uses **Whisper (Tiny)** model for high-quality Vietnamese transcription.
- **Text Post-Processing**: Automatically formats text with punctuation, line breaks, and readability improvements.
- **Simple Interface**: A user-friendly interface with a single "Record" button to start the conversion process.

## 🛠️ Technologies Used

- **Whisper (Tiny)**: Speech recognition for Vietnamese language.
- **Gemma 3n**: For text enhancement, ensuring smooth and efficient speech recognition with real-time performance.
- **Streamlit**: For building the interactive web interface.
- **Python**: Backend programming.

## 🚀 Installation

To get started with **Talk2TextVN**, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repo_url>
   ```
2. Install the required dependencies:
  ```bash
  pip install -r requirements.txt
  ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## 👥 Target Audience

This app is designed for:
- **Older Adults**: Providing an easy solution for those who are not comfortable with typing.
- **People with Hearing Impairments**: Offering an accessible transcription tool for the hearing-impaired community.
- **Users Unfamiliar with Typing**: Enabling a convenient voice-based interaction for individuals who prefer speaking over typing.

## 🎥 Video Demo

Check out the video demo of **Talk2TextVN** in action:

[Link to Video Demo]()

## 📝 License

This project is licensed under the MIT License.

## 🛠️ Troubleshooting

If you encounter issues while using the application, here are a few common solutions:

1. **Audio Not Recognized**: 
   - Make sure your microphone is correctly configured. If you're using a headset, check if the audio input is set to the correct device in your system settings.
   - Try restarting the application to reset any input devices.

2. **Dependencies Not Installed**:
   - Ensure that you've installed all the required dependencies with the following command:
     ```bash
     pip install -r requirements.txt
     ```

3. **Application Crashes**:
   - Check the error logs for missing files or incorrect versions of required libraries. You may want to check the version of **Whisper** or **Streamlit**.
   - Verify that your Python version is compatible with the dependencies. Recommended version: Python 3.7+.

4. **Performance Issues**:
   - If the app runs slowly, try reducing the audio input size or adjusting the model's parameters in the `config.py` file.
   - Consider running the application on a machine with better hardware for real-time speech recognition.

If you encounter other issues, please open a GitHub issue, and we'll assist you in resolving it.

## 🔧 Configuration

You can modify some parameters in the `config.py` file to adjust the application's performance:

- **Language Model Selection**: Choose between different Whisper models for varying levels of accuracy and speed.
- **Text Formatting Options**: Adjust how the final text output is processed. You can enable or disable features such as:
  - Line breaks after each sentence
  - Punctuation correction
  - Automatic paragraphing based on speech pauses

Example configuration:
```python
# config.py

# Model selection
whisper_model = 'whisper-tiny'  # Options: 'whisper-tiny', 'whisper-base', 'whisper-large'

# Text formatting options
line_breaks = True  # Enable/Disable line breaks after each sentence
punctuation = True  # Enable/Disable automatic punctuation
```

## 🤝 Contributing

If you'd like to contribute to this project, feel free to fork the repository, create a pull request, or open issues for any bugs or feature requests. Please ensure any pull requests follow the project's coding style and include tests where appropriate.

---
