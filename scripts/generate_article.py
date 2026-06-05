#!/usr/bin/env python3
"""
Generate weekly cat articles automatically using Gemini AI
"""
import os
import json
import re
from google import genai
from datetime import datetime
from pathlib import Path

# --- Setup ---
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
HISTORY_FILE = "article_history.json"

# Categories for index.html
CATEGORIES = {
    "behavior_psycho": {
        "title": "Behavior & Psychology",
        "display": "Behavior & Psychology",
        "directory": "content/behavior_psycho",
    },
    "breed_history": {
        "title": "Breeds & History",
        "display": "Breeds & History",
        "directory": "content/breed_history",
    },
    "around_world": {
        "title": "Around the World",
        "display": "Around the World",
        "directory": "content/around_world",
    },
    "culture": {
        "title": "Culture",
        "display": "Culture",
        "directory": "content/culture",
    },
}

# --- Load History ---
history = []
if os.path.exists(HISTORY_FILE):
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
    except Exception:
        pass


def generate_article_with_gemini():
    """Generate article using Gemini AI"""
    categories_list = ", ".join(CATEGORIES.keys())
    today = datetime.now().strftime('%Y-%m-%d')
    
    prompt = f"""Write a professional HTML article about cats.

Categories to choose from: {categories_list}

Instructions:
1. First, decide which category this article fits best.
2. Generate a compelling title for the article.
3. Write 2-3 paragraphs of engaging, informative content about cats.
4. Return ONLY valid HTML (no markdown, no frontmatter).
5. Start with: <h2 class="section-heading text-uppercase">TITLE HERE</h2>
6. Follow with: <p>paragraph content...</p> tags for each paragraph.
7. At the very beginning, on a single line, put: CATEGORY:category_name
8. At the very beginning before CATEGORY, put: TITLE:The Title Here

Example format:
TITLE:Why Cats Purr
CATEGORY:behavior_psycho
<h2 class="section-heading text-uppercase">Why Cats Purr</h2>
<p>Content here...</p>
<p>More content...</p>

Recent topics to avoid: {", ".join(history[-5:]) if history else "none"}
"""

    print("🤖 Consulting Gemini 3.0 Flash...")
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text.strip()


def parse_gemini_response(response_text):
    """Parse Gemini response to extract title, category, and HTML content"""
    lines = response_text.split("\n")
    title = ""
    category = ""
    html_content = ""
    
    # Find title and category
    for i, line in enumerate(lines):
        if line.startswith("TITLE:"):
            title = line.replace("TITLE:", "").strip()
        elif line.startswith("CATEGORY:"):
            category = line.replace("CATEGORY:", "").strip()
        elif line.startswith("<h2"):
            # Start of HTML content
            html_content = "\n".join(lines[i:])
            break
    
    # Validate category
    if category not in CATEGORIES:
        category = list(CATEGORIES.keys())[0]  # fallback to first category
    
    return title, category, html_content


def slugify(text):
    """Convert text to URL-friendly format"""
    return re.sub(r'[^\w\s-]', '', text).lower().strip().replace(' ', '_')


def create_full_html_page(title, html_content):
    """Create a full HTML page with the article content"""
    article_html = f"""<!DOCTYPE html>
<html lang="en">
  <head>

    <meta charset="utf-8">
    <title>All about cats | {title}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="keywords" content="Alexis Carbillet,Carbillet,Cats">
    <meta name="author" content="Alexis Carbillet">
 
    <!-- Control appearance when share by social media -->
    <meta property="og:title" content="All about cats | {title}" />
    <meta property="og:description" content="" />
    <meta property='og:url' content="https://cats.alexis-carbillet.com/" />
    <meta property="og:type" content="website" />

    <!-- Bootstrap core CSS -->
    <link href="../../vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

	<!-- Icon -->
	<link rel="shortcut icon" href="../../img/logo/fluff.jpg"/>
	
    <!-- Custom fonts for this template -->
    <link href="../../vendor/font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700" rel="stylesheet" type="text/css">
    <link href='https://fonts.googleapis.com/css?family=Kaushan+Script' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Droid+Serif:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
    <link href='https://fonts.googleapis.com/css?family=Roboto+Slab:400,100,300,700' rel='stylesheet' type='text/css'>

    <!-- Custom styles for this template -->
    <link href="../../css/structure.css" rel="stylesheet">

	<!-- Choice of languages -->
	<link rel="alternate" hreflang="x-default" href="https://cats.alexis-carbillet.com/" />


  </head>

  <body id="page-top">

    <!-- Navigation --> 
    <nav class="navbar navbar-expand-lg fixed-top" id="mainNav">
      <div class="container">
		<img src="../img/logo/fluff.jpg" width="5%" style="margin-right: 2%;" alt="">
		<button class="navbar-toggler navbar-toggler-right" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <i class="fa fa-bars"></i>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav text-uppercase ml-auto">
            <li class="nav-item">
				<a class="nav-link js-scroll-trigger" href="../../index.html">Main</a>
			</li>
			<li class="nav-item">
				<a class="nav-link js-scroll-trigger" href="#article">Article</a>
			</li>
            <li class="nav-item">
              <a class="nav-link js-scroll-trigger" href="#contact">Contact</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>


    <!-- Header -->
    <header class="masthead">
        <div class="container">		
            <div class="intro-text" style="padding-bottom: 50px;">
            <div class="intro-lead-in text-center" style="padding-top: 10%">
              <h1 style="display:inline; font-size: 35px; padding-left: 30px; font-style: normal; color: black;">{title.upper()}</h1>
			  <hr style="width: 350px; height: 1px; border:none;color:#bd64b4;background-color:#bd64b4;">
              This page contains an article about cats. Feel free to read it.
            </div>
        </div>
      </header>

<!-- ========================== ARTICLE SECTION ============================== -->

<section id="article" class="bg-light">
	<div class="container">
		<div class="row">
			<div class="col-xs-12 col-md-12 col-sm-12 col-lg-12 text-left">
				{html_content}
			</div>
		</div>
	</div>
</section>

<!-- ======================================================================= -->

<!-- ========================== CONTACT SECTION ============================== -->

<iframe id="contact" src="../../contact.html"  frameborder="0" scrolling="no" style="border: none; width: 100%; height: 140vh; max-height: 800px;"></iframe>

<!-- ======================================================================= -->

<!-- ======================= FOOTER SECTION ================================ -->
<footer>
    <div class="container">
      <div class="row">
          <div class="col-xs-3 col-md-3 col-sm-3 col-lg-3">
              <iframe src="../../copyright.html" frameborder="0" style="padding: 0%; max-height: 25px; background-color:#212529;"></iframe>
          </div>
          <div class="col-xs-7 col-md-7 col-sm-7 col-lg-7"></div>
          <p><a href="../../index.html">Main</a></p>
      </div>
    </div>
  </footer>

<!-- ======================================================================= -->

<!-- ======================== JAVASCRIPT SECTION =========================== -->

    <!-- Bootstrap core JavaScript -->
    <script src="../../vendor/jquery/jquery.min.js"></script>
	<script src="../../vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

    <!-- Plugin JavaScript -->
    <script src="../../vendor/jquery-easing/jquery.easing.min.js"></script>
	
    <!-- Custom scripts for this template -->
    <script src="../../js/structure.js"></script>
	<script src="../../js/portfolio.js"></script>

    <!-- Activate the bootstrap tooltip, must be after jQuery load -->
    <script>
    $(function () {{
      $('[data-toggle="tooltip"]').tooltip();
    }})
    </script>
	
<!-- ======================================================================= -->
  </body>

</html>
"""
    return article_html


def save_article(title, category, html_content):
    """Save article HTML file"""
    slug = slugify(title)
    directory = CATEGORIES[category]["directory"]
    filename = f"{slug}.html"
    
    filepath = Path(directory) / filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    full_html = create_full_html_page(title, html_content)
    filepath.write_text(full_html)
    return filepath, slug, filename, directory, category


def update_index_html(title, slug, filename, directory, category):
    """Update index.html with new article link"""
    index_path = Path("index.html")
    index_content = index_path.read_text()

    category_display = CATEGORIES[category]["display"]
    article_link = directory.replace("content/", "") + "/" + filename

    # Find the category section in index.html
    category_marker = f'href="content/{category}/'

    if category_marker in index_content:
        # Category exists, add article to it
        lines = index_content.split("\n")
        
        for i, line in enumerate(lines):
            if category_marker in line:
                # Found this category, now find where to insert
                for j in range(i, min(i + 20, len(lines))):
                    if "</div>" in lines[j]:
                        new_link = f'\t\t\t\t<a class="dropdown-item" href="{article_link}">{title}</a>'
                        lines.insert(j, new_link)
                        index_content = "\n".join(lines)
                        break
                break
    else:
        # Create new category
        new_category_html = f"""			<div class="btn-group">
				<button type="button" class="btn btn-secondary dropdown-toggle" data-toggle="dropdown" style="background-color: #bd64b4;">{category_display}</button>
				<div class="dropdown-menu" style="background-color: #bd64b4;">
				<a class="dropdown-item" href="{article_link}">{title}</a>
				</div>
			</div>"""

        # Find where to insert (after last btn-group)
        last_btn_group = index_content.rfind("</div>\n\t\t\t</div>")
        if last_btn_group > 0:
            insert_pos = last_btn_group + len("</div>")
            index_content = (
                index_content[:insert_pos]
                + "\n"
                + new_category_html
                + index_content[insert_pos:]
            )

    index_path.write_text(index_content)


def main():
    """Main function"""
    print("🐱 Generating weekly cat article with Gemini AI...")

    # Generate article with Gemini
    gemini_response = generate_article_with_gemini()
    
    # Parse response
    title, category, html_content = parse_gemini_response(gemini_response)
    print(f"📝 Title: {title}")
    print(f"📂 Category: {CATEGORIES[category]['display']}")

    # Save article file
    filepath, slug, filename, directory, category = save_article(title, category, html_content)
    print(f"✅ Article saved: {filepath}")

    # Update index.html
    update_index_html(title, slug, filename, directory, category)
    print(f"✅ Updated index.html")
    
    # Update history
    history.append(slug)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

    print("🎉 Article generation complete!")


if __name__ == "__main__":
    main()
