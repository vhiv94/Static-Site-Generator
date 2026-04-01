# How the SSG Works

1. Delete everything in the /public directory.
2. Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
3. Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
   1. Open the file and read its contents.
   2. Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
   3. Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
      - Raw markdown -> TextNode -> HTMLNode
   4. Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
   5. Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
   6. Write the full HTML string to a file for that page in the /public directory.