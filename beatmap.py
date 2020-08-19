import operator

class bm():
    def __init__(self, file_path):
        self.file_path = file_path
        self.unicode_title = True
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
        if "//" not in line[:2]:
            key = line.split(":")[0].strip()
            value = line.split(":")[1].strip()
            self.data[section][key] = value
            
    
    def _read2(self, section, line):
        if "//" not in line[:2]:
            self.data[section].append(line.split(","))
    
    def read(self):
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
            else:
                self._read2(current_section, line)
    
    def write(self, file_path):
        with open(file_path, "w+", encoding="UTF-8") as file:
            # Some maps don't seem to work if I write the old version, so let's just use new version then
            # old version → file.write(self.file_format + "\n\n")
            file.write(self.file_format_14 + "\n\n")
            # Writing every section
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
        # Finding uninherited timing points, storing [(time, beattime)]
        uninherited_timing_points_times = [(value[0], value[1]) for value in self.data["[TimingPoints]"] if value[6] == "1"]
        # Finding the differences between subsequent bpms = length of timing point, appending [time, length, bpm]
        diffs = []
        for value in enumerate(uninherited_timing_points_times):
            # Calculating timing_point[i+1] - timing_point[i]
            # If IndexError = this is the last value, don't forget to calculate it too
            try:
                diffs.append([uninherited_timing_points_times[value[0]][0], float(uninherited_timing_points_times[value[0] + 1][0]) - float(uninherited_timing_points_times[value[0]][0]), round(1 / float(uninherited_timing_points_times[value[0]][1]) * 1000 * 60)])
            except IndexError:
                diffs.append([uninherited_timing_points_times[value[0]][0], int(self.data["[HitObjects]"][-1][2]) - float(uninherited_timing_points_times[value[0]][0]), round(1 / float(uninherited_timing_points_times[value[0]][1]) * 1000 * 60)])
                break
        # Creating bpm_lengths that is [bpm, length]
        bpm_lengths = []
        bpms = []
        for value in diffs:
            if value[2] in bpms:
                bpm_lengths[bpms.index(value[2])][1] += value[1]
            else:
                bpms.append(value[2])
                bpm_lengths.append([value[2], value[1]])
        # Finally finding the main bpm
        bpm = max(bpm_lengths, key=operator.itemgetter(1))[0]
        print(bpm)
        return bpm
