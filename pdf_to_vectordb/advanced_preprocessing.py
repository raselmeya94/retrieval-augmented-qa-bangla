import re
# Bengali and Devanagari digits mapping (optional for normalization)
bn_digit_map = str.maketrans("0123456789", "০১২৩৪৫৬৭৮৯")
dev_digit_map = str.maketrans("०१२३४५६७८९", "০১২৩৪৫৬৭৮৯")

# Hindi to Bengali character mapping
hindi_to_bengali_map = {
    "क": "ক", "ख": "খ", "ग": "গ", "घ": "ঘ", "च": "চ", "छ": "ছ", "ज": "জ",
    "झ": "ঝ", "ञ": "ঞ", "ट": "ট", "ठ": "ঠ", "ड": "ড", "ढ": "ঢ", "ण": "ণ",
    "त": "ত", "थ": "থ", "द": "দ", "ध": "ধ", "न": "ন", "प": "প", "फ": "ফ",
    "ब": "ব", "भ": "ভ", "म": "ম", "य": "য", "र": "র", "ल": "ল", "व": "ব",
    "श": "শ", "ष": "ষ", "स": "স", "ह": "হ", "ळ": "ল", "क्ष": "ক্ষ", "ज्ञ": "জ্ঞ",
}

# Function to replace Hindi characters with Bengali ones and handle digits
def convert_hindi_to_bengali(raw_text):
    # Step 1: Replace Hindi characters with Bengali ones
    for hindi_char, bengali_char in hindi_to_bengali_map.items():
        raw_text = raw_text.replace(hindi_char, bengali_char)

    # Step 2: Translate digits to Bengali numerals
    raw_text = raw_text.translate(bn_digit_map).translate(dev_digit_map)
    
    return raw_text

# Function to extract and clean up answers from the raw text
def extract_answers(raw_text):
    # Step 1: Apply the Hindi-to-Bengali conversion
    corrected_text = convert_hindi_to_bengali(raw_text)
    return corrected_text


def bangla_to_english_digit(bn_digit):
    bn_en_map = str.maketrans('০১২৩৪৫৬৭৮৯', '0123456789')
    return bn_digit.translate(bn_en_map)

def english_to_bangla_digit(en_digit_str):
    en_bn_map = str.maketrans('0123456789', '০১২৩৪৫৬৭৮৯')
    return en_digit_str.translate(en_bn_map)

# def fix_serial_numbers(text):
#     start_trigger = '| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |'
#     end_trigger = '# সৃজনশীল প্রশ্ন'

#     in_correction_mode = False
#     corrected_lines = []
#     serial_counter = 1

#     for line in text.splitlines():
#         if start_trigger in line:
#             in_correction_mode = True
#             serial_counter = 1
#             corrected_lines.append(line)
#             continue

#         if end_trigger in line:
#             in_correction_mode = False
#             corrected_lines.append(line)
#             continue

#         if in_correction_mode and "|" in line:
#             tokens = [token.strip() for token in line.strip('|').split('|')]
#             new_tokens = []
#             i = 0
#             while i < len(tokens):
#                 if i % 2 == 0:  # SL column
#                     try:
#                         num_eng = int(bangla_to_english_digit(tokens[i]))
#                         if num_eng != serial_counter:
#                             new_tokens.append(english_to_bangla_digit(str(serial_counter)))
#                         else:
#                             new_tokens.append(tokens[i])
#                     except ValueError:
#                         new_tokens.append(english_to_bangla_digit(str(serial_counter)))
#                     serial_counter += 1
#                 else:  # Ans column
#                     new_tokens.append(tokens[i])
#                 i += 1

#             while len(new_tokens) < 10:
#                 if len(new_tokens) % 2 == 0:
#                     new_tokens.append(english_to_bangla_digit(str(serial_counter)))
#                     serial_counter += 1
#                 else:
#                     new_tokens.append('')

#             fixed_line = "| " + " | ".join(new_tokens) + " |"
#             corrected_lines.append(fixed_line)
#         else:
#             corrected_lines.append(line)

#     return "\n".join(corrected_lines)
import re

def fix_serial_numbers(text):
    start_trigger = '২ চচবযाনा'
    end_trigger = 'সৃজনশীল প্রশ্ন'

    in_correction_mode = False
    corrected_lines = []
    serial_counter = 1

    def bangla_to_english_digit(bn):
        mapping = {'০':'0','১':'1','২':'2','৩':'3','৪':'4','৫':'5','৬':'6','৭':'7','৮':'8','৯':'9'}
        return ''.join([mapping.get(c, c) for c in bn])

    def english_to_bangla_digit(en):
        mapping = {'0':'০','1':'১','2':'২','3':'৩','4':'৪','5':'৫','6':'৬','7':'৭','8':'৮','9':'৯'}
        return ''.join([mapping.get(c, c) for c in en])

    for line in text.splitlines():
        if start_trigger in line:
            in_correction_mode = True
            serial_counter = 1
            corrected_lines.append(line)
            continue

        if end_trigger in line:
            in_correction_mode = False
            corrected_lines.append(line)
            continue

        if in_correction_mode and re.search(r'[০-৯]+ [কখগঘ]', line):
            tokens = re.findall(r'([০-৯]+)\s*([কখগঘ])', line)
            new_line = []
            for sl, ans in tokens:
                expected_sl = english_to_bangla_digit(str(serial_counter))
                new_line.append(f"{expected_sl} {ans}")
                serial_counter += 1
            corrected_lines.append(" ".join(new_line))
        else:
            corrected_lines.append(line)

    return "\n".join(corrected_lines)


mcq_answers = {
    "১": "ক", "২": "খ", "৩": "ক", "৪": "গ", "৫": "ক",
    "৬": "গ", "৭": "ক", "৮": "খ", "৯": "খ", "১০": "খ",
    "১১": "খ", "১২": "ক", "১৩": "গ", "১৪": "খ", "১৫": "গ",
    "১৬": "গ", "১৭": "খ", "১৮": "খ", "১৯": "গ", "২০": "ঘ",
    "২১": "ঘ", "২২": "ক", "২৩": "ঘ", "২৪": "ক", "২৫": "ঘ",
    "২৬": "খ", "২৭": "ক", "২৮": "ক", "২৯": "গ", "৩০": "ক",
    "৩১": "গ", "৩২": "খ", "৩৩": "খ", "৩৪": "ক", "৩৫": "ঘ",
    "৩৬": "খ", "৩৭": "ক", "৩৮": "গ", "৩৯": "গ", "৪০": "খ",
    "৪১": "গ", "৪২": "ক", "৪৩": "ক", "৪৪": "গ", "৪৫": "খ",
    "৪৬": "খ", "৪৭": "খ", "৪৮": "খ", "৪৯": "খ", "৫০": "খ",
    "৫১": "ঘ", "৫২": "গ", "৫৩": "গ", "৫৪": "খ", "৫৫": "খ",
    "৫৬": "খ", "৫৭": "গ", "৫৮": "ক", "৫৯": "ক", "৬০": "ঘ",
    "৬১": "ক", "৬২": "খ", "৬৩": "ক", "৬৪": "ক", "৬৫": "খ",
    "৬৬": "ক", "৬৭": "ক", "৬৮": "খ", "৬৯": "গ", "৭০": "ঘ",
    "৭১": "খ", "৭২": "গ", "৭৩": "ঘ", "৭৪": "ক", "৭৫": "গ",
    "৭৬": "গ", "৭৭": "গ", "৭৮": "গ", "৭৯": "খ", "৮০": "খ",
    "৮১": "খ", "৮২": "গ", "৮৩": "ঘ", "৮৪": "খ", "৮৫": "ঘ",
    "৮৬": "গ", "৮৭": "ক", "৮৮": "খ", "৮৯": "ক", "৯০": "ঘ",
    "৯১": "খ", "৯২": "ঘ", "৯৩": "ঘ", "৯৪": "ক", "৯৫": "খ",
    "৯৬": "খ", "৯৭": "ক", "৯৮": "ঘ", "৯৯": "ঘ", "১০০": "ঘ"
}




# def mcq_answering(text):
#     lines = text.split("\n")
    
#     corrected_text = []
#     current_question_number = None
#     in_mcq_section = False
#     start_trigger = "১। রবীন্দ্রনাথ ঠাকুরের জীবনাবসান ঘটে কোথায়?"
#     end_trigger = "২ চচবযाনा"

#     for line in lines:
#         stripped_line = line.strip()

#         # Step 0: Activate MCQ section if start line is found
#         if not in_mcq_section and stripped_line == start_trigger:
#             in_mcq_section = True
#             corrected_text.append(line)
#             continue

#         # Step 0.5: Stop MCQ section if end line is found
#         if in_mcq_section and stripped_line == end_trigger:
#             in_mcq_section = False
#             corrected_text.append(line)
#             continue

#         # If not in MCQ section, just add the line
#         if not in_mcq_section:
#             corrected_text.append(line)
#             continue

#         # Step 1: Detect question number
#         match_question = re.match(r"^(\d+)।", stripped_line)
#         # print(match_question)
#         if match_question:
#             current_question_number = match_question.group(1)
#             # print(match_question)
#             corrected_text.append(line)
#             continue

#         # Step 2: Add the option lines
#         corrected_text.append(line)

#         # Step 3: If this is the last option (ঘ), add the answer
#         if stripped_line.startswith("(ঘ)"):
#             answer = mcq_answers.get(current_question_number)
#             if answer:
#                 corrected_text.append(f"\nউত্তরঃ {answer}\n")

#     return "\n".join(corrected_text)


import re

def mcq_answering(text):
    lines = text.split("\n")
    
    corrected_text = []
    current_question_number = None
    current_options = {}
    in_mcq_section = False

    start_trigger = "১। রবীন্দ্রনাথ ঠাকুরের জীবনাবসান ঘটে কোথায়?"
    end_trigger = "২ চচবযाনा"

    for line in lines:
        stripped_line = line.strip()

        # Step 0: Activate MCQ section if start line is found
        if not in_mcq_section and stripped_line == start_trigger:
            in_mcq_section = True
            corrected_text.append(line)
            continue

        # Step 0.5: Stop MCQ section if end line is found
        if in_mcq_section and stripped_line == end_trigger:
            in_mcq_section = False
            corrected_text.append(line)
            continue

        # If not in MCQ section, just add the line
        if not in_mcq_section:
            corrected_text.append(line)
            continue

        # Step 1: Detect question number
        match_question = re.match(r"^(\d+)।", stripped_line)
        if match_question:
            # নতুন প্রশ্ন শুরু হলে, আগের অপশনগুলো রিসেট করো
            current_question_number = match_question.group(1)
            current_options = {}
            corrected_text.append(line)
            continue

        # Step 2: Detect MCQ option lines like (ক) ঢাকা
        match_option = re.match(r"^\((ক|খ|গ|ঘ)\)\s*(.+)", stripped_line)
        if match_option:
            opt_label = match_option.group(1)
            opt_text = match_option.group(2)
            current_options[opt_label] = opt_text
            corrected_text.append(line)

            # Step 3: If this is the last option (ঘ), add the answer
            if opt_label == "ঘ":
                answer_letter = mcq_answers.get(current_question_number)
                if answer_letter and answer_letter in current_options:
                    answer_text = current_options[answer_letter]
                    corrected_text.append(f"\nউত্তরঃ {answer_letter} ({answer_text})\n")

            continue

        # Step 4: Any other line
        corrected_text.append(line)

    return "\n".join(corrected_text)
