import sys
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtWidgets import QApplication, QFileDialog
from beatmap import bm
import subprocess
import os

from copy import deepcopy


class Program():
    def __init__(self):
        # For convenience, later will make auto detection ↓
        self.osu_directory = r"D:\Games\osu!\Songs"
        # Streamcompanion integration - loads in-game selected beatmaps automatically
        self.selected_now = r"C:\Program Files (x86)\StreamCompanion\Files\selected_now.txt"
        self.file_path = ""
        self.initUI()

    def initUI(self):
        self.app = QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = uic.loadUi(self.resource_path("mainwindow.ui"), self.MainWindow)
        self.MainWindow.setFixedSize(self.MainWindow.size())
        self.ui.chooseDirectoryButton.clicked.connect(lambda: self.loadBeatmap(True))
        self.ui.changeRateButton.clicked.connect(self.changeSpeed)
        self.ui.changeBpmButton.clicked.connect(self.changeSpeed)
        if os.path.isfile(self.selected_now):
            fs_watcher = QtCore.QFileSystemWatcher(self.MainWindow)
            fs_watcher.addPath(self.selected_now)
            fs_watcher.fileChanged.connect(self.file_changed)
    
    def resource_path(self, relative_path):
        # PyInstaller compatibility
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def file_changed(self):
        with open(self.selected_now, "r", encoding="UTF-8") as file:
            self.file_path = file.read().strip()
        self.loadBeatmap(False)

    def loadBeatmap(self, clicked):
        if clicked:
            self.file_path = QFileDialog.getOpenFileName(self.MainWindow, directory=self.osu_directory)[0]
        if self.file_path:
            os.chdir(os.path.dirname(self.file_path))
            self.ui.pathLineEdit.setText(self.file_path)
            self.beatmap = bm(self.file_path)
            self.beatmap.audio_name = self.beatmap.data["[General]"]["AudioFilename"][:-4]
            self.beatmap.input_audio_path = self.beatmap.data["[General]"]["AudioFilename"]
            self.beatmap.version_file = self.file_path[self.file_path.rfind("[")+1:self.file_path.rfind("]")]
            self.beatmap.version = self.beatmap.data["[Metadata]"]["Version"]
            self.beatmap.bpm = self.beatmap.find_bpm()
            self.ui.bpmSpinBox.setRange(0, 1000)
            self.ui.bpmSpinBox.setValue(self.beatmap.bpm)
            self.ui.bpmSpinBox.setMinimum(int(self.beatmap.bpm * 0.5))
            self.ui.bpmSpinBox.setMaximum(int(self.beatmap.bpm * 2))

    def changeSpeed(self):
        if self.ui.rateDoubleSpinBox.value() != 1.0 or self.ui.bpmSpinBox.value() != self.beatmap.bpm:
            self.new_beatmap = deepcopy(self.beatmap)
            if self.ui.changeBpmButton.isChecked():
                self.speed_rate = round(self.ui.bpmSpinBox.value() / self.new_beatmap.bpm, 4)
                self.output_audio_path = f"{self.new_beatmap.audio_name}_{self.ui.bpmSpinBox.value()}.mp3"
                self.new_beatmap.data["[General]"]["AudioFilename"] = f"{self.new_beatmap.audio_name}_{self.ui.bpmSpinBox.value()}.mp3"
                self.new_beatmap.data["[Metadata]"]["Version"] = f"{self.new_beatmap.version} [{self.ui.bpmSpinBox.value()} BPM]"
            else:
                self.speed_rate = round(self.ui.rateDoubleSpinBox.value(), 2)
                self.output_audio_path = f"{self.new_beatmap.audio_name}_x{self.speed_rate}.mp3"
                self.new_beatmap.data["[General]"]["AudioFilename"] = f"{self.new_beatmap.audio_name}_x{self.speed_rate}.mp3"
                self.new_beatmap.data["[Metadata]"]["Version"] = f"{self.new_beatmap.version} x{self.speed_rate}"
            # Creating new audio file
            if self.ui.pitchCheckBox.isChecked():
                sample_rate = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "stream=sample_rate", "-of", "default=noprint_wrappers=1:nokey=1", self.new_beatmap.input_audio_path], text=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()
                subprocess.call(["ffmpeg", "-i",
                                self.beatmap.input_audio_path,
                                "-filter:a",
                                f"asetrate={sample_rate}*{self.speed_rate},aresample={sample_rate}",
                                "-vn",
                                self.output_audio_path,
                                "-y"], stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.call(["ffmpeg", "-i",
                                self.beatmap.input_audio_path,
                                "-filter:a",
                                f"atempo={self.speed_rate}",
                                "-vn",
                                self.output_audio_path,
                                "-y"], stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NO_WINDOW)
            # Actually changing speed
            self.new_beatmap.data["[General]"]["PreviewTime"] = str(round(float(self.new_beatmap.data["[General]"]["PreviewTime"]) / self.speed_rate))
            if self.new_beatmap.data["[Editor]"].get("Bookmarks"):
                self.new_beatmap.data["[Editor]"]["Bookmarks"] = ",".join([str(round(int(value) / self.speed_rate)) for value in self.new_beatmap.data["[Editor]"]["Bookmarks"].split(",")])
            if self.new_beatmap.data["[General]"].get("AudioLeadIn"):
                self.new_beatmap.data["[General]"]["AudioLeadIn"] = str(round(int(self.new_beatmap.data["[General]"]["AudioLeadIn"]) / self.speed_rate))
            for timing_point in self.new_beatmap.data["[TimingPoints]"]:
                timing_point[0] = str(round(float(timing_point[0]) / self.speed_rate))
                if timing_point[6] == "1":
                    timing_point[1] = str(float(timing_point[1]) / self.speed_rate)
            for hit_object in self.new_beatmap.data["[HitObjects]"]:
                hit_object[2] = str(round(int(hit_object[2]) / self.speed_rate))
                if "1" in format(int(hit_object[3]), "b").zfill(8)[-4]:
                    hit_object[5] = str(round(int(hit_object[5]) / self.speed_rate))
            for event in self.new_beatmap.data["[Events]"]:
                if event[0] ==  "0":
                    continue
                elif event[0] == "1" or event[0] == "Video":
                    event[1] = str(round(int(event[1]) / self.speed_rate))
                elif event[0] == "2" or event[0] == "Break":
                    event[1] = str(round(int(event[1]) / self.speed_rate))
                    event[2] = str(round(int(event[2]) / self.speed_rate))
            # I am too lazy to fix storyboard, maybe I'll do it later
            storyboard_related = ["Sprite", "Animation", " F", " M", " S", " V", " R", " C", " L", " T", " P"]
            self.new_beatmap.data["[Events]"] = [value for value in self.new_beatmap.data["[Events]"] if value[0] not in storyboard_related]
            # Adjusting AR/OD
            if self.ui.adjustCheckBox.isChecked():
                original_od = float(self.new_beatmap.data["[Difficulty]"]["OverallDifficulty"])
                modified_hitwindow = (79.5 - 6 * original_od) / self.speed_rate
                modified_od = round((79.5 - modified_hitwindow) / 6, 1)
                self.new_beatmap.data["[Difficulty]"]["OverallDifficulty"] = str(modified_od)
                if self.new_beatmap.data["[Difficulty]"].get("ApproachRate"):
                    original_ar = float(self.new_beatmap.data["[Difficulty]"]["ApproachRate"])
                    if original_ar > 5:
                        modified_ar = round((1950 - (1200 - 150 * (original_ar - 5)) / self.speed_rate) / 150, 1)
                    else:
                        modified_ar = round((1950 - (1200 + 120 * (5 - original_ar)) / self.speed_rate) / 150, 1)
                    self.new_beatmap.data["[Difficulty]"]["ApproachRate"] = str(modified_ar)
            # Writing to new .osu file
            if self.ui.changeBpmButton.isChecked():
                self.new_beatmap.write(f"{self.file_path[:self.file_path.rfind(self.new_beatmap.version_file)] + self.new_beatmap.version_file} [{self.ui.bpmSpinBox.value()} BPM]].osu")
            else:
                self.new_beatmap.write(f"{self.file_path[:self.file_path.rfind(self.new_beatmap.version_file)] + self.new_beatmap.version_file} x{self.speed_rate}].osu")
        self.ui.changeRateButton.setChecked(False)
        self.ui.changeBpmButton.setChecked(False)


if __name__ == "__main__":
    program = Program()
    program.MainWindow.show()
    sys.exit(program.app.exec_())
