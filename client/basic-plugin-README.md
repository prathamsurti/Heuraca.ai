# Basic Figma Plugin with API Integration

This is a minimal Figma plugin that allows you to:
1. Inspect selected Figma elements
2. Send the element data to an API
3. Cancel the plugin

## Files

- `basic-plugin.html` - The UI for the plugin (no CSS styling)
- `basic-plugin.js` - The plugin code that runs in Figma
- `basic-plugin-manifest.json` - The manifest file for the plugin

## How to Use

1. Import the plugin into Figma:
   - Create a new plugin in Figma
   - Select "From manifest..."
   - Choose the `basic-plugin-manifest.json` file

2. Run the plugin:
   - Select elements in your Figma design
   - Click "Inspect Elements" to see their details
   - Enter an API URL (default is http://127.0.0.1:8000/audit-data)
   - Click "Send to API" to send the data
   - Click "Cancel" to close the plugin

## Features

- **Minimal UI**: Just the essential elements with no styling
- **Element Inspection**: Shows basic information about selected elements
- **API Integration**: Sends element data to a specified API endpoint
- **Recursive Display**: Shows nested elements in a hierarchical structure

## API Data Format

The data sent to the API has the following structure:

```json
{
  "elements": [
    {
      "id": "element-id",
      "type": "FRAME",
      "name": "Element Name",
      "children": [
        {
          "id": "child-id",
          "type": "TEXT",
          "name": "Text Element",
          "text": {
            "content": "Text content",
            "length": 12
          }
        }
      ]
    }
  ]
}
```

## Development

This is a basic implementation with minimal features. To extend it:

1. Modify `basic-plugin.html` to add more UI elements or styling
2. Update `basic-plugin.js` to extract more properties from Figma elements
3. Update the manifest file if needed

No build step is required for this basic version.
