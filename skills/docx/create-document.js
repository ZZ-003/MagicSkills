const { Document, Packer, Paragraph, TextRun, AlignmentType, HeadingLevel } = require('docx');
const fs = require('fs');

// Create a professional document with proper styling
const doc = new Document({
  styles: {
    default: { 
      document: { 
        run: { font: "Arial", size: 24 } // 12pt default font
      } 
    },
    paragraphStyles: [
      // Override built-in Title style
      { 
        id: "Title", 
        name: "Title", 
        basedOn: "Normal",
        run: { size: 56, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 120 }, alignment: AlignmentType.CENTER } 
      },
      // Override built-in heading styles
      { 
        id: "Heading1", 
        name: "Heading 1", 
        basedOn: "Normal", 
        next: "Normal", 
        quickFormat: true,
        run: { size: 32, bold: true, color: "000000", font: "Arial" },
        paragraph: { spacing: { before: 240, after: 240 }, outlineLevel: 0 } 
      }
    ]
  },
  sections: [{
    properties: { 
      page: { 
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } // 1 inch margins
      } 
    },
    children: [
      new Paragraph({ 
        heading: HeadingLevel.TITLE, 
        children: [new TextRun("Sample Document")] 
      }),
      new Paragraph({ 
        heading: HeadingLevel.HEADING_1, 
        children: [new TextRun("Introduction")] 
      }),
      new Paragraph({
        children: [
          new TextRun("This is a professionally formatted Word document created using the docx library. It demonstrates proper styling, formatting, and structure following best practices.")
        ]
      }),
      new Paragraph({
        children: [
          new TextRun("Key features of this document:")
        ]
      }),
      new Paragraph({ 
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Professional Arial font throughout")] 
      }),
      new Paragraph({ 
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Proper heading hierarchy with outline levels")] 
      }),
      new Paragraph({ 
        numbering: { reference: "bullet-list", level: 0 },
        children: [new TextRun("Consistent spacing and margins")] 
      })
    ]
  }]
});

// Configure numbering for bullet points
doc.numbering = {
  config: [
    { 
      reference: "bullet-list",
      levels: [{ 
        level: 0, 
        format: "bullet", 
        text: "•", 
        alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 720, hanging: 360 } } } 
      }] 
    }
  ]
};

// Save the document
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("sample-document.docx", buffer);
  console.log("Document created successfully as 'sample-document.docx'");
});
