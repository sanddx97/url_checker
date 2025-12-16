# KRAG Template Master Reference Guide
## The Complete Manual for Report Design

> [!NOTE]
> **How to Use This Guide**
> This guide is structured to help you understand and use every feature of the KRAG system.
> For each feature, we follow this pattern:
> 1.  **Functionality**: What is it?
> 2.  **Usage**: How do I write the code?
> 3.  **Example**: Show me a snippet.
>
> **At the end of this document, you will find a complete, copy-pasteable End-to-End Template.**

---

# 1. Introduction: The "Binder" Concept

### Functionality
Before writing code, visualize your report as a physical **Ring Binder**.
*   **Workbook**: The binder itself.
*   **Sheets**: The pages inside.
*   **Containers**: The boxes you draw on a page.
*   **Components**: The content (Text, Images, Tables) inside the boxes.

### Usage
You build a template by nesting these elements in XML:
`Workbook -> Sheet -> Container -> Component`

---

# 2. The Workbook (Root)

### Functionality
The Workbook is the root of your template. It defines the output file name, format, and data source.

### Usage
The `<Template>` tag must be the first line of your file.

| Attribute | Required | Description | Allowed Values |
| :--- | :--- | :--- | :--- |
| `type` | **Yes** | Defines this as a workbook. | `WORKBOOK` |
| `fileName` | **Yes** | Name of the output file. | Any text (no extension) |
| `fileFormat` | **Yes** | The output format. | `XLSX`, `PDF`, `CSV`, `ZIP` |
| `dataSource` | **Yes** | Where data comes from. | `TABLEAU`, `MANUAL`, `API` |

### Example
```xml
<Template type="WORKBOOK" fileName="Q4_Sales_Report" fileFormat="XLSX" dataSource="TABLEAU">
    <!-- Content goes here -->
</Template>
```

---

# 3. Global Styles

### Functionality
Styles define how your content looks (Fonts, Colors, Borders). Defining them globally lets you reuse them, keeping your code clean.

### Usage
Define `<style>` blocks inside `<globalStyles>`. Use the `id` attribute to name them.

### Style Properties Reference

#### A. Font (`<font>`)
| Attribute | Description | Example |
| :--- | :--- | :--- |
| `fontName` | Font family name. | `Arial`, `Calibri` |
| `size` | Font size in points. | `11`, `14`, `24` |
| `bold` | Bold text. | `true` |
| `italic` | Italic text. | `true` |
| `underline` | Underline text. | `true` |
| `strikeout` | Strikethrough (cross out) text. | `true` |
| `color` | Hex color code. | `#FF0000` (Red) |

#### B. Border (`<border>`)
| Attribute | Description | Example |
| :--- | :--- | :--- |
| `style` | Line style. | `THIN`, `THICK`, `DOTTED`, `DASHED`, `DOUBLE` |
| `color` | Hex color code. | `#000000` |
| `thickness` | Line thickness (1-3). | `1` |
| `top` | Apply to top edge. | `true` |
| `bottom` | Apply to bottom edge. | `true` |
| `left` | Apply to left edge. | `true` |
| `right` | Apply to right edge. | `true` |

#### C. Fill (`<fill>`)
| Attribute | Description | Example |
| :--- | :--- | :--- |
| `foregroundColor` | Background color. | `#FFFF00` (Yellow) |
| `pattern` | Fill pattern. | `SOLID` (Default), `NONE` |

#### D. Alignment (`<alignment>`)
| Attribute | Description | Example |
| :--- | :--- | :--- |
| `horizontal` | Left/Right alignment. | `LEFT`, `CENTER`, `RIGHT`, `JUSTIFY` |
| `vertical` | Top/Bottom alignment. | `TOP`, `CENTER`, `BOTTOM` |
| `wrapping` | Text wrapping behavior. | `WRAP`, `OVERFLOW`, `CLIP` |

#### E. Format (`<format>`)
Excel format string for numbers/dates.
*   `#,##0.00` (Currency)
*   `0.00%` (Percentage)
*   `yyyy-mm-dd` (Date)
*   `@` (Text)

### Example
```xml
<globalStyles>
    <style id="header_style">
        <font fontName="Arial" size="12" bold="true" underline="true" color="#FFFFFF"/>
        <fill foregroundColor="#0000FF"/>
        <alignment horizontal="CENTER" vertical="CENTER" wrapping="WRAP"/>
        <border style="THIN" thickness="2" color="#000000" bottom="true"/>
    </style>
</globalStyles>
```

---

# 4. Sheets & Configuration

### Functionality
A Sheet represents a single tab in an Excel workbook or a page in a PDF. You can configure page settings like gridlines and print layout.

### Usage
Use `<sheet>` to create a page and `<sheetConfig>` for settings.

| Tag | Description | Default |
| :--- | :--- | :--- |
| `<showGridLines>` | Show Excel gridlines. | `true` |
| `<zoomScale>` | Zoom percentage. | `100` |
| `<printSetup>` | Orientation and paper size. | `PORTRAIT`, `A4` |

### Example
```xml
<sheets>
    <sheet name="Summary Dashboard">
        <sheetConfig>
            <showGridLines>false</showGridLines>
            <zoomScale>85</zoomScale>
            <printSetup>
                <orientation>LANDSCAPE</orientation>
                <paperSize>A4</paperSize>
            </printSetup>
        </sheetConfig>
        <!-- Containers go here -->
    </sheet>
</sheets>
```

---

# 5. Layout & Containers

### Functionality
Containers are the boxes that hold your content.
*   **GROUP**: A structural box that holds *other containers*. Used for organizing sections (e.g., "Header Section").
*   **LEAF**: A content box that holds *one component*. Used for actual items (Text, Image, Table).

### Usage
Every sheet needs one root **GROUP** container. Inside, you place other containers using **Coordinates** (R1, C1, R2, C2).

## 5.1 Deep Dive: Relative Positioning

Relative positioning allows you to place a box based on the position of another box. This is crucial for dynamic reports where the size of a table or text might change.

### The Concept: Anchor + Offset
Think of it like giving directions: "Go to the **Bottom** of the Logo, then go **Down 1 Step**."

*   **Anchor**: The reference point (e.g., `logo.R2`).
*   **Offset**: The adjustment (e.g., `1`).

### The Syntax
We use a nested `<item>` structure to perform the math: `Anchor + Offset`.

```xml
<r1Expression>
    <item>
        <item>
            <item>TARGET_ID.COORDINATE</item> <!-- The Anchor -->
            <item>OFFSET_NUMBER</item>      <!-- The Offset -->
        </item>
    </item>
</r1Expression>
```

### Available Coordinates
*   `TARGET.R1`: Top Row of the target.
*   `TARGET.R2`: Bottom Row of the target.
*   `TARGET.C1`: Left Column of the target.
*   `TARGET.C2`: Right Column of the target.

### Layout Cookbook (Common Patterns)

#### Pattern A: Place BELOW (The most common)
"Start my top row (R1) one row after the target's bottom row (R2)."
```xml
<r1Expression>
    <item><item><item>header.R2</item><item>1</item></item></item>
</r1Expression>
```

#### Pattern B: Place to the RIGHT
"Start my left column (C1) one column after the target's right column (C2)."
```xml
<c1Expression>
    <item><item><item>sidebar.C2</item><item>1</item></item></item>
</c1Expression>
```

#### Pattern C: Align TOPS
"Start my top row (R1) at the same row as the target's top row (R1)."
```xml
<r1Expression>
    <item><item><item>sidebar.R1</item></item></item> <!-- No offset needed -->
</r1Expression>
```

#### Pattern D: Full Width BELOW
"Start below the header, start at column 0, and end at column 10."
```xml
<relativePosition>
    <!-- Row: Below Header -->
    <r1Expression><item><item><item>header.R2</item><item>1</item></item></item></r1Expression>
    
    <!-- Columns: Hardcoded 0 to 10 -->
    <!-- Note: You can mix relative rows with absolute columns! -->
</relativePosition>
<position c1="0" c2="10"/> <!-- Define columns here -->
```

### Example
```xml
<!-- 1. The Header Group -->
<container type="GROUP" id="header_section">
    <position r1="0" c1="0"/> <!-- Starts at top-left -->
    <containers>
        
        <!-- Logo (Leaf) -->
        <container type="LEAF" id="logo_box">
            <position r1="0" c1="0" r2="2" c2="2"/> <!-- 3x3 box -->
            <component type="IMAGE" source="logo.png"/>
        </container>

        <!-- Title (Leaf) - Positioned to the RIGHT of Logo -->
        <container type="LEAF" id="title_box">
            <relativePosition>
                <!-- Start Column = Logo's End Column + 1 -->
                <c1Expression><item><item><item>logo_box.C2</item><item>1</item></item></item></c1Expression>
                <!-- Start Row = Logo's Start Row -->
                <r1Expression><item><item><item>logo_box.R1</item></item></item></r1Expression>
            </relativePosition>
            <component type="TEXT" content="Sales Report"/>
        </container>

    </containers>
</container>
```

---

# 6. Components

## 6.1 Text Component

### Functionality
Displays static text.

### Usage
Use `type="TEXT"`.

### Example
```xml
<component type="TEXT" content="Confidential Report" styleId="header_style"/>
```

## 6.2 Image Component

### Functionality
Displays an image from a URL or file path.

### Usage
Use `type="IMAGE"`.

| Attribute | Description |
| :--- | :--- |
| `source` | URL or File Path. |
| `scale` | Resize factor (e.g., `0.5` for 50%). |

### Example
```xml
<component type="IMAGE" source="https://example.com/logo.png" scale="0.8"/>
```

## 6.3 Table Component (The Powerhouse)

### Functionality
Displays data in a grid. It connects to your data source (e.g., Tableau) and maps fields to rows and columns.

### Usage
A table consists of:
1.  **Column Groups**: Horizontal headers (e.g., Years).
2.  **Row Groups**: Vertical headers (e.g., Categories).
3.  **Data Fields**: The numbers in the middle.

### Example
```xml
<component type="TABLE" id="sales_table">
    
    <!-- Columns: Years -->
    <columnGroups>
        <columnGroup id="years">
            <headerFields>
                <headerField id="year_header">
                    <labelConfig headerLabel="Year"/>
                    <valueConfig dataType="TEXT">
                        <valueSource><sourceInfos><sourceInfo field="Year" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </headerField>
            </headerFields>
            
            <!-- Data: Sales Numbers -->
            <dataFields>
                <dataField id="sales_data">
                    <labelConfig headerLabel="Revenue"/>
                    <valueConfig dataType="FLOAT" operation="SUM">
                        <valueSource><sourceInfos><sourceInfo field="Sales" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </dataField>
            </dataFields>
        </columnGroup>
    </columnGroups>

    <!-- Rows: Categories -->
    <rowGroups>
        <rowGroup id="categories">
            <headerFields>
                <headerField id="cat_header">
                    <labelConfig headerLabel="Category"/>
                    <valueConfig dataType="TEXT">
                        <valueSource><sourceInfos><sourceInfo field="Category" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </headerField>
            </headerFields>
        </rowGroup>
    </rowGroups>

</component>
```

---

# 7. Appendix: Reference Values

### Data Types (`dataType`)
*   `TEXT`: Strings.
*   `INT`: Whole numbers.
*   `FLOAT`: Decimals.
*   `DATE`: Dates.
*   `PERCENTAGE`: Percent values (0.1 = 10%).

### Operations (`operation`)
*   `SUM`: Total.
*   `AVG`: Average.
*   `COUNT`: Count items.
*   `MIN` / `MAX`: Extremes.
*   `NONE`: Raw data.

---

# 8. Full End-to-End Template

Here is a complete, working template that combines everything. You can copy this file and use it as a starter.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Template type="WORKBOOK" fileName="Executive_Summary" fileFormat="XLSX" dataSource="TABLEAU">

    <!-- 1. GLOBAL STYLES -->
    <globalStyles>
        <!-- Title Style: Big, Blue, Bold -->
        <style id="title_style">
            <font fontName="Calibri" size="24" bold="true" color="#1F4E78"/>
            <alignment horizontal="CENTER" vertical="CENTER"/>
        </style>
        
        <!-- Header Style: Blue Background, White Text -->
        <style id="header_style">
            <font fontName="Calibri" size="11" bold="true" color="#FFFFFF"/>
            <fill foregroundColor="#4472C4"/>
            <border style="THIN" color="#000000" top="true" bottom="true" left="true" right="true"/>
            <alignment horizontal="CENTER" vertical="CENTER"/>
        </style>

        <!-- Data Style: Currency Format -->
        <style id="currency_style">
            <font fontName="Calibri" size="11" color="#000000"/>
            <alignment horizontal="RIGHT" vertical="CENTER"/>
            <format>#,##0.00</format> <!-- $1,234.56 -->
            <border style="THIN" color="#D9D9D9" top="true" bottom="true" left="true" right="true"/>
        </style>
    </globalStyles>

    <!-- 2. SHEETS -->
    <sheets>
        <sheet name="Sales Dashboard">
            
            <!-- Page Configuration -->
            <sheetConfig>
                <showGridLines>false</showGridLines>
                <zoomScale>90</zoomScale>
            </sheetConfig>

            <!-- 3. ROOT CONTAINER -->
            <container type="GROUP" id="root">
                <position r1="0" c1="0"/>
                <containers>

                    <!-- A. HEADER SECTION -->
                    <container type="GROUP" id="header_group">
                        <position r1="0" c1="0"/>
                        <containers>
                            
                            <!-- Logo -->
                            <container type="LEAF" id="logo">
                                <position r1="1" c1="1" r2="3" c2="2"/>
                                <component type="IMAGE" source="https://example.com/logo.png" scale="0.5"/>
                            </container>

                            <!-- Title (Relative to Logo) -->
                            <container type="LEAF" id="title">
                                <relativePosition>
                                    <c1Expression><item><item><item>logo.C2</item><item>1</item></item></item></c1Expression>
                                    <r1Expression><item><item><item>logo.R1</item></item></item></r1Expression>
                                </relativePosition>
                                <component type="TEXT" content="Q4 Executive Sales Report" styleId="title_style"/>
                            </container>

                        </containers>
                    </container>

                    <!-- B. DATA TABLE (Relative to Header) -->
                    <container type="LEAF" id="table_container">
                        <relativePosition>
                            <r1Expression><item><item><item>header_group.R2</item><item>2</item></item></item></r1Expression>
                            <c1Expression><item><item><item>header_group.C1</item><item>1</item></item></item></c1Expression>
                        </relativePosition>

                        <component type="TABLE" id="main_table">
                            <title type="TEXT" content="Sales by Region &amp; Year">
                                <style><font bold="true" size="14"/></style>
                            </title>

                            <tableConfig showColumnHeader="true" showRowHeader="true" mergeDuplicateRows="true"/>

                            <!-- Columns: Years -->
                            <columnGroups>
                                <columnGroup id="cg_years">
                                    <headerFields>
                                        <headerField id="year">
                                            <labelConfig headerLabel="Year" styleId="header_style"/>
                                            <valueConfig dataType="TEXT">
                                                <valueSource><sourceInfos><sourceInfo field="Year" sourceId="SalesData"/></sourceInfos></valueSource>
                                                <style><alignment horizontal="CENTER"/></style>
                                            </valueConfig>
                                        </headerField>
                                    </headerFields>
                                    <dataFields>
                                        <dataField id="sales">
                                            <labelConfig headerLabel="Revenue" styleId="header_style"/>
                                            <valueConfig dataType="FLOAT" operation="SUM" styleId="currency_style">
                                                <valueSource><sourceInfos><sourceInfo field="Sales" sourceId="SalesData"/></sourceInfos></valueSource>
                                            </valueConfig>
                                        </dataField>
                                    </dataFields>
                                </columnGroup>
                            </columnGroups>

                            <!-- Rows: Regions -->
                            <rowGroups>
                                <rowGroup id="rg_regions">
                                    <headerFields>
                                        <headerField id="region">
                                            <labelConfig headerLabel="Region" styleId="header_style"/>
                                            <valueConfig dataType="TEXT">
                                                <valueSource><sourceInfos><sourceInfo field="Region" sourceId="SalesData"/></sourceInfos></valueSource>
                                                <style><font bold="true"/></style>
                                            </valueConfig>
                                        </headerField>
                                    </headerFields>
                                </rowGroup>
                            </rowGroups>

                        </component>
                    </container>

                </containers>
            </container>
        </sheet>
    </sheets>

</Template>
```
