import xml.etree.ElementTree as ET
import argparse

# Register namespaces to preserve prefixes in output
ET.register_namespace('', 'http://www.w3.org/2005/Atom')
ET.register_namespace('g', 'http://base.google.com/ns/1.0')

G_NS = 'http://base.google.com/ns/1.0'
ATOM_NS = 'http://www.w3.org/2005/Atom'


def process_feed(input_path: str, output_path: str) -> None:
    """
    Parse the Shoper XML feed and set all <g:condition> to 'refurbished'.
    For entries without <g:identifier_exists>, insert one with 'no'.

    :param input_path: Path to the input XML file
    :param output_path: Path to save the modified XML file
    """
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Iterate through each entry
    for entry in root.findall(f'{{{ATOM_NS}}}entry'):
        # Find and update <g:condition>
        cond = entry.find(f'{{{G_NS}}}condition')
        if cond is not None:
            cond.text = 'refurbished'
        
        # Check for <g:identifier_exists>
        id_exists = entry.find(f'{{{G_NS}}}identifier_exists')
        if id_exists is None:
            new_id_exists = ET.Element(f'{{{G_NS}}}identifier_exists')
            new_id_exists.text = 'no'
            if cond is not None:
                idx = list(entry).index(cond)
                entry.insert(idx + 1, new_id_exists)
            else:
                entry.append(new_id_exists)
        else:
            id_exists.text = 'no'

    # Write out the updated feed
    tree.write(output_path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process Shoper feed for Google Merchant Center.')
    parser.add_argument('input', help='Input XML file (Shoper feed)')
    parser.add_argument('output', help='Output XML file path')
    args = parser.parse_args()

    process_feed(args.input, args.output)
    print(f'Processed feed saved to: {args.output}')
