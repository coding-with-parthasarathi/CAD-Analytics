import streamlit as st
import ezdxf

def extract_metadata_from_dxf(file):
    """Extract metadata from a DXF file using ezdxf."""
    try:
        # Save the file temporarily for processing
        with open("temp.dxf", "wb") as f:
            f.write(file.getbuffer())

        # Load DXF file using ezdxf
        dxf_doc = ezdxf.readfile("temp.dxf")

        # Extract various entity counts
        block_count = len(dxf_doc.blocks)
        line_count = len(dxf_doc.modelspace().query("LINE"))
        arc_count = len(dxf_doc.modelspace().query("ARC"))
        polyline_count = len(dxf_doc.modelspace().query("LWPOLYLINE POLYLINE"))
        viewport_count = len(dxf_doc.viewports)
        dimension_count = len(dxf_doc.modelspace().query("DIMENSION"))

        # Extract units (if available)
        units = dxf_doc.header.get('$INSUNITS', 'Unknown')

        # Extract author (if available)
        author = dxf_doc.header.get('$LASTSAVEDBY', 'Unknown')

        # Initialize a list to store extracted text
        extracted_text = []

        # Query for TEXT and MTEXT entities in the modelspace
        for entity in dxf_doc.modelspace().query("TEXT MTEXT"):
            if entity.dxftype() == "TEXT":
                extracted_text.append(f"{entity.dxf.text.strip()}")
            elif entity.dxftype() == "MTEXT":
                extracted_text.append(f"{entity.text.strip()}")

        # Format the extracted text into a structured format
        formatted_text = "\n".join(extracted_text)
        # Extract metadata
        metadata = {
            "File Format": "DXF",
            "Entities Count": len(dxf_doc.entities),
            "Layers Count": len(dxf_doc.layers),
            "Block Definitions Count": block_count,
            "Line Entities Count": line_count,
            "Arc Entities Count": arc_count,
            "Polyline Entities Count": polyline_count,
            "Dimensions Count": dimension_count,
            "Viewport Count": viewport_count,
            "Units": units,
            "File Version": dxf_doc.header["$ACADVER"],
            "Author": author,
            "Creation Date": dxf_doc.header.get('$TDCREATE', 'Unknown'),
            "Modification Date": dxf_doc.header.get('$TDUPDATE', 'Unknown'),
            "Texts detected": formatted_text
        }

        return metadata
    except Exception as e:
        return {"Error": str(e)}

def process_dxf(file):
    """Process DXF file."""
    file_name = file.name.lower()

    if file_name.endswith(".dxf"):
        return extract_metadata_from_dxf(file)
    else:
        return {"Error": "Unsupported file format. Please upload a DWG or DXF file."}

# Streamlit app
st.title("DXF File Metadata Extractor")

# Allow user to upload a single DWG or DXF file
uploaded_file = st.file_uploader("Upload a DXF file", type=["dxf"], accept_multiple_files=False)

if uploaded_file:
    st.write(f"**Processing file:** {uploaded_file.name}")
    
    # Process the file (DWG or DXF)
    metadata = process_dxf(uploaded_file)

    # Display metadata
    st.subheader(f"Metadata for {uploaded_file.name}")
    st.json(metadata)