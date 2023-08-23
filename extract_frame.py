import cv2
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QWidget

class FrameExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("MP4 to JPG Frame Extractor")

        self.input_path_label = QLabel("Input MP4 Path:")
        self.input_path_entry = QLineEdit()
        self.input_path_button = QPushButton("Browse")
        self.input_path_button.clicked.connect(self.browse_input_path)

        self.output_path_label = QLabel("Output JPG Path:")
        self.output_path_entry = QLineEdit()
        self.output_path_button = QPushButton("Browse")
        self.output_path_button.clicked.connect(self.browse_output_path)

        self.extract_button = QPushButton("Extract Frames")
        self.extract_button.clicked.connect(self.extract_frames)

        self.status_label = QLabel("")

        layout = QVBoxLayout()
        layout.addWidget(self.input_path_label)
        layout.addWidget(self.input_path_entry)
        layout.addWidget(self.input_path_button)
        layout.addWidget(self.output_path_label)
        layout.addWidget(self.output_path_entry)
        layout.addWidget(self.output_path_button)
        layout.addWidget(self.extract_button)
        layout.addWidget(self.status_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_input_path(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(filter="MP4 files (*.mp4)")
        self.input_path_entry.setText(file_path)

    def browse_output_path(self):
        dir_dialog = QFileDialog()
        dir_path = dir_dialog.getExistingDirectory()
        self.output_path_entry.setText(dir_path)

    def extract_frames(self):
        input_video_path = self.input_path_entry.text()
        output_frame_dir = self.output_path_entry.text()

        os.makedirs(output_frame_dir, exist_ok=True)

        cap = cv2.VideoCapture(input_video_path)

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_path = os.path.join(output_frame_dir, f'frame_{frame_count:04d}.jpg')
            cv2.imwrite(frame_path, frame)

            frame_count += 1

        cap.release()
        self.status_label.setText('Frame extraction complete!')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FrameExtractorApp()
    window.show()
    sys.exit(app.exec_())
