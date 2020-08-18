class bm():
    def __init__(self, file_path):
        self.file_path = file_path
        self.unicode_title = True
        self.file_format = ""
        self.file_format_14 = "osu file format v14"
        self.data = {}
        self.possible_sections = ("[General]", "[Editor]", "[Metadata]", "[Difficulty]", "[Events]", "[TimingPoints]", "[Colours]", "[HitObjects]")
        self.sections_one = ("[General]", "[Editor]", "[Metadata]", "[Difficulty]", "[Colours]")
        self.sections_two = ("[Events]", "[TimingPoints]", "[HitObjects]")
        self.read()

    def __repr__(self):
        # Artist - Song name [Difficulty name]
        if self.unicode_title and self.data["[Metadata]"].get("ArtistUnicode") and self.data["[Metadata]"].get("TitleUnicode"):
            return f"{self.data['[Metadata]']['ArtistUnicode']} - {self.data['[Metadata]']['TitleUnicode']} [{self.data['[Metadata]']['Version']}]"
        return f"{self.data['[Metadata]']['Artist']} - {self.data['[Metadata]']['Title']} [{self.data['[Metadata]']['Version']}]"

    def _lines_clean(self, lines):
        lines = [value.rstrip() for value in lines]
        lines = [value for value in lines if value]
        self.file_format = lines[0]
        lines = lines[1:]
        return lines

    def _read1(self, section, line):
        if "//" in line:
            pass
        else:
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            self.data[section][key] = value
    
    def _read2(self, section, line):
        if "//" in line:
            pass
        else:
            self.data[section].append(line.split(","))
    
    def read(self):
        # Reading lines from file and cleaning them
        with open(self.file_path, "r", encoding="UTF-8") as file:
            lines = file.readlines()
        lines = self._lines_clean(lines)
        current_section = ""
        for line in lines:
            if line in self.possible_sections:
                current_section = line
                if line in self.sections_one:
                    self.data[current_section] = {}
                else:
                    self.data[current_section] = []
                continue
            if current_section in self.sections_one:
                self._read1(current_section, line)
            elif current_section in self.sections_two:
                self._read2(current_section, line)
            else:
                print("WHAT")
    
    def write(self, file_path):
        with open(file_path, "w+", encoding="UTF-8") as file:
            # Some maps doesn't seem to work if I write the old version, so let's just use new version then
            # The old version → file.write(self.file_format + "\n\n")
            file.write(self.file_format_14 + "\n\n")
            # Write every section
            for section in self.possible_sections:
                if section in self.sections_one:
                    if section == "[Colours]":
                        if self.data.get(section):
                            file.write(section + "\n")
                            for key in self.data[section].keys():
                                file.write(key + " : " + self.data[section][key] + "\n")
                        else:
                            continue
                    elif section == "[Metadata]" or section == "[Difficulty]":
                        file.write(section + "\n")
                        for key in self.data[section].keys():
                            file.write(key + ":" + self.data[section][key] + "\n")
                    else:
                        file.write(section + "\n")
                        for key in self.data[section].keys():
                            file.write(key + ": " + self.data[section][key] + "\n")
                    file.write("\n")
                else:
                    file.write(section + "\n")
                    for lvalue in self.data[section]:
                        file.write(",".join(lvalue) + "\n")
                    file.write("\n")
    
    def find_bpm(self):
        # Am I stupid for making it so complicated, or am I a genius and actully did it right? I don't know at this point...
        uninherited_timing_points_times = [value[0] for value in self.data["[TimingPoints]"] if value[6] == "1"]
        diffs = []
        for value in enumerate(uninherited_timing_points_times):
            try:
                diffs.append((uninherited_timing_points_times[value[0]], int(uninherited_timing_points_times[value[0] + 1]) - int(uninherited_timing_points_times[value[0]])))
            except IndexError:
                diffs.append((uninherited_timing_points_times[value[0]], int(self.data["[HitObjects]"][-1][2]) - int(uninherited_timing_points_times[value[0]])))
                break
        max = [0, 0]
        for value in enumerate(diffs):
            if diffs[value[0]][1] > max[1]:
                max[0] = diffs[value[0]][0]
                max[1] = diffs[value[0]][1]
        time_max = max[0]
        bpm = 0
        for value in self.data["[TimingPoints]"]:
            if value[6] == "1" and value[0] == str(time_max):
                bpm = round(1 / float(value[1]) * 1000 * 60)
        # Actually we still need to take into account that bpm can repeat: 200→220→200, and add times up.
        # I think I will add this later.
        return bpm
