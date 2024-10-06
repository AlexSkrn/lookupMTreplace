import argparse
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

def parse_terms(file_path):
    """Parses a single .txt file and returns two lists: regex and plain text terms."""
    regex_list = []
    plain_text_list = []

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for line in lines:
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue  # Ignore lines that do not have at least 2 columns
        find_text = parts[0]
        replace_text = parts[1]

        # Add to regex_list as tuple
        if len(parts) == 2:
            regex_list.append((find_text, replace_text))

        # If there's a third element, add find/replace pair to plain_text_list
        elif len(parts) >= 3 and parts[2].strip():
            plain_text_list.append((find_text, replace_text))

    return regex_list, plain_text_list

def sort_terms(regex_list, plain_text_list):
    """Sorts the terms by the length of the first element in each tuple."""
    regex_list.sort(key=lambda x: len(x[0]), reverse=True)
    plain_text_list.sort(key=lambda x: len(x[0]), reverse=True)
    return regex_list, plain_text_list

def generate_xml(regex_list, plain_text_list, output_path):
    """Generates a pretty-printed XML file from the provided regex and plain text lists."""
    root = ET.Element("EditCollection")
    items_element = ET.SubElement(root, "Items")

    for find_text, replace_text in regex_list:
        edit_item = ET.SubElement(items_element, "EditItem", 
                                   Enabled="true", EditItemType="regular_expression")
        ET.SubElement(edit_item, "FindText").text = f'\\b{find_text}\\b'
        ET.SubElement(edit_item, "ReplaceText").text = replace_text

    for find_text, replace_text in plain_text_list:
        edit_item = ET.SubElement(items_element, "EditItem", 
                                   Enabled="true", EditItemType="plain_text")
        ET.SubElement(edit_item, "FindText").text = find_text
        ET.SubElement(edit_item, "ReplaceText").text = replace_text

    # Convert the ElementTree to a string and pretty-print it
    xml_string = ET.tostring(root, encoding='utf-8')
    parsed_xml = minidom.parseString(xml_string)
    pretty_xml_string = parsed_xml.toprettyxml(indent="\t")
    
    # Remove the first line with XML declaration
    pretty_xml_string = '\n'.join(pretty_xml_string.split('\n')[1:])

    # Write the pretty-printed XML to the output file
    with open(output_path, 'w', encoding='utf-8') as xml_file:
        xml_file.write(pretty_xml_string)

def main():
    parser = argparse.ArgumentParser(description='Process .txt files for term replacements.')
    parser.add_argument('input_files', type=str, nargs='+', help='Input .txt files with terms for find and replace.')

    args = parser.parse_args()

    # Ensure all input files have a .txt extension
    for input_file in args.input_files:
        if not input_file.endswith('.txt'):
            print(f"Input file {input_file} must have a .txt extension.")
            return

    # Initialize lists to hold merged results
    regex_list, plain_text_list = [], []

    # Parse each input file and merge results
    for input_file in args.input_files:
        r_list, p_list = parse_terms(input_file)
        regex_list.extend(r_list)
        plain_text_list.extend(p_list)

    # Convert to sets to remove duplicates
    regex_list = list(set(regex_list))
    plain_text_list = list(set(plain_text_list))

    regex_list, plain_text_list = sort_terms(regex_list, plain_text_list)

    # Create output file name based on the first input file
    output_file = os.path.splitext(args.input_files[0])[0] + '.xml'
    generate_xml(regex_list, plain_text_list, output_file)
    print(f"XML file generated: {output_file}")

if __name__ == "__main__":
    main()
