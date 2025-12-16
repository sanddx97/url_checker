# KRAG Template Design User Guide
## A Beginner's Guide to Creating Beautiful Reports

> [!TIP]
> **Who is this guide for?**
> This guide is for anyone who wants to design reports using the KRAG system. **No programming knowledge is required.** If you can sketch a layout on a piece of paper, you can create a KRAG template!

---

## 1. Introduction: The "Binder" Analogy

Before we look at any code, let's visualize how a KRAG report is built. Think of your report like a physical **Ring Binder**.

1.  **The Workbook (The Binder)**: This is the file itself (e.g., `Sales_Report.xlsx`). It holds everything together.
2.  **Sheets (The Pages)**: Inside the binder, you have pages (tabs in Excel). You can have one page or many.
3.  **Containers (The Boxes)**: On each page, you draw rectangular **boxes** to organize your content.
    *   Some boxes are just for grouping things together (like a "Header" section).
    *   Some boxes hold the actual content.
4.  **Components (The Content)**: Inside the boxes, you put your actual content:
    *   **Text**: Titles, paragraphs, labels.
    *   **Images**: Logos, diagrams.
    *   **Tables**: The actual data grids.

**The Golden Rule:** Every piece of content MUST live inside a Container (Box). You cannot just float text on a page; it needs a box!

---

## 2. Getting Started: Your First "Hello World"

Let's look at the simplest possible template. This creates an Excel file with one sheet and one title.

```xml
<Template type="WORKBOOK" fileName="my_first_report" fileFormat="XLSX">
    
    <!-- The Pages -->
    <sheets>
        <sheet name="Summary">
            
            <!-- The Root Box (Holds everything on the page) -->
            <container type="GROUP" id="root">
                <position r1="0" c1="0"/> <!-- Starts at top-left -->
                
                <containers>
                    <!-- A Box for our Title -->
                    <container type="LEAF" id="title_box">
                        <!-- Position: Row 0, Col 0 to Row 1, Col 5 -->
                        <position r1="0" c1="0" r2="1" c2="5"/>
                        
                        <!-- The Content -->
                        <component type="TEXT" content="Hello World!"/>
                    </container>
                </containers>
                
            </container>
        </sheet>
    </sheets>
    
</Template>
```

**What just happened?**
1.  We created a **Workbook** named `my_first_report`.
2.  We added a **Sheet** named "Summary".
3.  We added a **Root Container** (the main layout area).
4.  Inside that, we put a **Leaf Container** (a content box) at the top-left.
5.  Inside the box, we put a **Text Component** saying "Hello World!".

---

## 3. The Building Blocks

### 3.1 Containers: The Boxes
There are only two types of boxes you need to know:

| Type | Name | Purpose | Analogy |
| :--- | :--- | :--- | :--- |
| **GROUP** | Group Container | Holds *other containers*. Used for layout and organization. | A drawer divider. It doesn't hold socks directly; it holds smaller boxes for socks. |
| **LEAF** | Leaf Container | Holds *one component*. Used for actual content. | The sock box. You put the actual socks (content) inside it. |

### 3.2 Components: The Content
There are three main types of content you can put in a Leaf Container:

#### A. Text
Simple text for titles, descriptions, or notes.
```xml
<component type="TEXT" content="Monthly Sales Report"/>
```

#### B. Image
Pictures, logos, or icons. You can load them from a website (URL) or a file.
```xml
<component type="IMAGE" source="https://example.com/logo.png" scale="0.5"/>
```
*   `scale="0.5"` means "50% of original size".

#### C. Table
The powerhouse! Displays data in rows and columns. (We will cover this in detail in Section 6).

---

## 4. Styling Your Report: Make it Pretty

Nobody likes boring reports. You can define **Global Styles** at the top of your template and use them anywhere. It's like creating a "Theme".

### Step 1: Define the Style
```xml
<globalStyles>
    <style>
        <id>my_fancy_title</id> <!-- Give it a unique name -->
        
        <!-- Font Settings -->
        <font fontName="Arial" size="24" bold="true" color="#FF0000"/>
        
        <!-- Alignment -->
        <alignment horizontal="CENTER" vertical="CENTER"/>
        
        <!-- Background Color -->
        <fill foregroundColor="#FFFF00"/> <!-- Yellow background -->
        
        <!-- Borders -->
        <border style="THIN" color="#000000" bottom="true"/>
    </style>
</globalStyles>
```

### Step 2: Use the Style
Add `styleId="my_fancy_title"` to any component.
```xml
<component type="TEXT" content="WARNING" styleId="my_fancy_title"/>
```

### Style Cheat Sheet
*   **Colors**: Use Hex codes (e.g., `#FFFFFF` for white, `#000000` for black, `#FF0000` for red).
*   **Alignments**: `LEFT`, `CENTER`, `RIGHT`, `TOP`, `BOTTOM`.
*   **Borders**: `THIN`, `THICK`, `DOTTED`, `DASHED`.

---

## 5. Layout: Where Does it Go?

Placing boxes on the page is done using **Coordinates**.
*   **R1**: Start Row (0 is the top)
*   **C1**: Start Column (0 is the left, i.e., Column A)
*   **R2**: End Row
*   **C2**: End Column

### 5.1 Absolute Positioning (Hard Coded)
"Put this box exactly at Row 5, Column 2."
```xml
<position r1="5" c1="2" r2="6" c2="4"/>
```
*   **Pros**: Easy to understand.
*   **Cons**: If you move the box above it, this one stays put and might overlap.

### 5.2 Relative Positioning (Smart Layout)
"Put this box 1 row below the `title_box`."
This is **highly recommended**. It makes your layout flexible.

```xml
<relativePosition>
    <!-- Start Row: Take title_box's bottom row (R2) and add 1 -->
    <r1Expression>
        <item><item><item>title_box.R2</item><item>1</item></item></item>
    </r1Expression>
    
    <!-- Start Column: Same as title_box's start column (C1) -->
    <c1Expression>
        <item><item><item>title_box.C1</item></item></item>
    </c1Expression>
</relativePosition>
```
*   **Pros**: If `title_box` gets bigger, this box moves down automatically!

---

## 6. Mastering Tables: The Data Grid

Tables are the most important part of a report. They connect to your data (like Tableau) and show it.

### The Anatomy of a Table
A table is split into two groups:
1.  **Column Groups**: What goes across the top? (e.g., Years, Months, Metrics)
2.  **Row Groups**: What goes down the side? (e.g., Product Categories, Regions)

### Example: Sales by Year and Category

**Goal**:
| | 2023 | 2024 |
| :--- | :--- | :--- |
| **Electronics** | $500 | $600 |
| **Furniture** | $200 | $300 |

### The Code
```xml
<component type="TABLE" id="sales_table">
    
    <!-- 1. Define Columns (The Years) -->
    <columnGroups>
        <columnGroup id="years">
            <headerFields>
                <headerField id="year_header">
                    <labelConfig headerLabel="Year"/> <!-- The word "Year" -->
                    <valueConfig dataType="TEXT">
                        <!-- Get "Year" field from Tableau -->
                        <valueSource><sourceInfos><sourceInfo field="Year" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </headerField>
            </headerFields>
            
            <!-- The Data Inside the Columns (Sales Numbers) -->
            <dataFields>
                <dataField id="sales_data">
                    <labelConfig headerLabel="Sales"/>
                    <valueConfig dataType="FLOAT" operation="SUM"> <!-- Sum up the numbers -->
                        <valueSource><sourceInfos><sourceInfo field="Sales" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </dataField>
            </dataFields>
        </columnGroup>
    </columnGroups>
    
    <!-- 2. Define Rows (The Categories) -->
    <rowGroups>
        <rowGroup id="categories">
            <headerFields>
                <headerField id="cat_header">
                    <labelConfig headerLabel="Category"/>
                    <valueConfig dataType="TEXT">
                        <!-- Get "Category" field from Tableau -->
                        <valueSource><sourceInfos><sourceInfo field="Category" sourceId="TableauSheet"/></sourceInfos></valueSource>
                    </valueConfig>
                </headerField>
            </headerFields>
        </rowGroup>
    </rowGroups>
    
</component>
```

### Key Table Settings
You can control how the table behaves using `<tableConfig>`:
*   `mergeDuplicateRows="true"`: If "Electronics" appears twice, merge them into one big cell.
*   `showColumnHeader="true"`: Show the gray header row at the top.
*   `showRowHeader="true"`: Show the gray header column on the left.

---

## 7. Reference Guide

### 7.1 Supported Data Types
When mapping data, tell the system what kind of data it is:
*   `TEXT`: Names, IDs, descriptions.
*   `INT`: Whole numbers (1, 50, 100).
*   `FLOAT`: Decimals (10.50, 99.99).
*   `DATE`: Dates (2023-12-25).
*   `PERCENTAGE`: Percent values (0.5 for 50%).

### 7.2 Operations (Math)
What should we do with the numbers?
*   `SUM`: Add them up (Total Sales).
*   `AVG`: Calculate average (Average Price).
*   `COUNT`: Count how many items.
*   `MIN` / `MAX`: Find the smallest or largest number.
*   `NONE`: Just show the raw data.

### 7.3 Formatting Codes
Use these in `<style><format>...</format></style>`:
*   `#,##0.00` -> 1,234.56 (Standard Currency)
*   `0%` -> 50% (Percentage)
*   `yyyy-mm-dd` -> 2023-12-31 (Date)
*   `dd/mm/yyyy` -> 31/12/2023 (UK Date)

---

> [!NOTE]
> **Need Help?**
> If your template isn't working, check:
> 1.  Did you close all your tags? (e.g., `<container>...</container>`)
> 2.  Are your IDs unique? (You can't have two boxes named "title_box")
> 3.  Is your data source connected?

Happy Reporting!
