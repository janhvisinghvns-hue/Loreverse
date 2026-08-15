# Loreverse

## Overview

Loreverse is a Django-based web application designed for readers and writers of fiction. Rather than functioning as a simple story publishing website, Loreverse combines storytelling with world-building to create an interactive fictional universe that readers can explore.

The central idea behind Loreverse is that a story can contain much more than its chapters. A fictional world can have its own characters, locations, creatures, history, images, and other pieces of lore. Loreverse allows writers to create and organize these elements alongside their stories, while readers can explore them while reading or separately through the World Explorer.

The application supports two roles: Readers and Writers. Every registered user begins as a Reader and can choose to become a Writer. Writers retain all reader functionality while gaining the ability to create, edit, publish, and manage stories and their associated worlds.

Readers can discover published stories, search for stories or authors, filter stories by genre and tags, maintain personal reading lists, continue stories from the chapter where they stopped, view their reading history, mark stories as completed, favorite stories, and interact with chapters through likes and comments.

Loreverse is built using Django on the backend, SQLite for the database, HTML templates and CSS for the interface, Bootstrap for responsive layout, and JavaScript for interactive frontend functionality.

## Distinctiveness and Complexity

Loreverse is distinct from the other CS50W projects because its primary purpose is neither social networking nor e-commerce. Instead, it combines a fiction reading platform with a structured world-building system.

The application is not a social network like Project 4. Although readers can like and comment on chapters, social interaction is not the central purpose of the website. Loreverse does not revolve around following users, maintaining a social feed, or connecting users with one another. User accounts instead exist to provide personalized reading and writing functionality. A reader can maintain favorites, a Want to Read collection, completed stories, reading history, and continue-reading information. Writers use their accounts to manage stories, chapters, and fictional worlds.

Loreverse is also not an e-commerce application like Project 2. The application does not center around products, shopping carts, checkout, or purchasing. Its primary interaction is with fictional content rather than commercial products. The focus is on reading, writing, organizing, discovering, and exploring fictional universes.

The main feature that distinguishes Loreverse is the **World Explorer**. A conventional story website might associate a story with chapters, a title, description, author, and cover image. Loreverse goes further by allowing every story to have an associated fictional world. A world can contain a description and images, as well as characters, locations, creatures, and timeline events. Characters, locations, and creatures can each have their own images, while timeline events can document important events in the world's history.

This creates a structured relationship between the story and its lore:

**Story → World → Characters, Locations, Creatures, Images, and Timeline Events**

The World Explorer allows readers to explore this information without having to find every detail inside the chapters themselves. This makes the fictional universe a separate interactive layer of the application rather than simply treating world-building information as ordinary story text.

The application also has a personalized reading system. Loreverse stores the relationship between a user, a story, and the chapter they are reading. This allows the Continue Reading section to return a reader to the appropriate chapter rather than simply showing the last story they opened. The application also maintains reading history and completed stories, while separate relationships allow users to mark stories as favorites or add them to their Want to Read collection.

The database therefore contains interconnected models for profiles, stories, chapters, worlds, characters, locations, creatures, timeline events, images, reading information, likes, and comments. These relationships allow different parts of the application to work together rather than operating as independent pages.

Writers also have their own management interface. A writer can create a story as a draft, add chapters, create its world, add world-building information, edit the story, publish it, and view engagement information such as chapter likes and comments. Published stories then become available through the public discovery interface.

JavaScript is also used for several interactive features throughout the application. It provides light and dark theme switching, chapter text-size controls, confirmation before deleting stories, and an image lightbox in the World Explorer. In the World Explorer, clicking an image displays it prominently against a darkened background, allowing readers to inspect world-building artwork without leaving the page.

The application is also designed to be mobile-responsive. Bootstrap's responsive layout is combined with custom CSS for story cards, navigation, forms, typography, spacing, continue-reading cards, filtering interfaces, and other parts of the application. This allows Loreverse to provide a consistent experience across different screen sizes.

For these reasons, Loreverse is more than a CRUD-based story application. It combines authentication and role management, story and chapter management, personalized reading state, content discovery, community interaction, and a structured world-building system into a single application.

## Features

### Authentication and Profiles

* User registration, login, and logout
* Reader profiles
* Ability for a Reader to become a Writer
* Writer and Reader role-based functionality
* Profile picture
* User biography
* Profile editing
* Password changing

### Story and Chapter Management

Writers can:

* Create stories
* Save stories as drafts
* Edit stories
* Delete stories
* Publish stories
* Create chapters
* View their stories and their publication status
* View story engagement information
* Access the story's World Explorer

Stories contain a title, genre, tags, description, cover image, author, publication status, and timestamps.

### Reading Features

Readers can:

* Browse published stories
* Open story details
* Read individual chapters
* Navigate between chapters
* Continue reading from their previous chapter
* Favorite stories
* Add stories to Want to Read
* Mark stories as completed
* View reading history
* Access a personalized Reader Dashboard

### Discovery

Users can discover content through:

* Published Stories
* Genre-based sections
* Genre filters
* Tag filters
* Story search
* Author search

The home page also presents story cards and Continue Reading cards with cover images.

### World Explorer

Every story can have a fictional world containing:

* World description
* World images
* Characters
* Character images
* Locations
* Location images
* Creatures
* Creature images
* Timeline events

The World Explorer provides a separate way to understand and explore the lore behind a story.

### Chapter Interaction

Readers can:

* Like chapters
* Comment on chapters
* Adjust chapter text size using `A-`, `A`, and `A+`

Writers can see the number of likes and comments associated with their stories.

### Frontend Interactivity

JavaScript is used for:

* Dark/light theme switching
* Chapter text-size controls
* Story deletion confirmation
* World Explorer image lightbox functionality

## Database Models

Loreverse uses Django models to represent the application's interconnected data.

The main models include:

* `Profile` — stores user role, biography, and profile picture.
* `Story` — stores story information, author, publication status, genres, tags, images, and reader collections.
* `Chapter` — stores chapters belonging to stories.
* `World` — stores the world associated with a story.
* `WorldImage` — stores images associated with a world.
* `Character` and `CharacterImage` — represent characters and their images.
* `Location` and `LocationImage` — represent locations and their images.
* `Creature` and `CreatureImage` — represent creatures and their images.
* `TimelineEvent` — stores important historical events within a world.
* `ReadingProgress` — stores a user's current chapter for a story.
* `ReadingHistory` — stores stories a user has previously read.
* `CompletedStory` — stores stories a user has completed.
* `ChapterLike` — stores chapter likes while preventing duplicate likes from the same user.
* `ChapterComment` — stores comments made on chapters.

Several models use unique constraints to prevent duplicate relationships, such as a user having multiple reading-progress records for the same story or liking the same chapter more than once.

## File Structure

The project contains a Django application with templates, static files, models, views, and supporting project files.

### Templates

The application includes templates for:

* `layout.html` — base layout and shared navigation
* `index.html` — Loreverse home page
* `login.html` — login page
* `register.html` — registration page
* `profile.html` — user profile
* `become_writer.html` — Reader-to-Writer conversion
* `change_password.html` — password management
* `create_story.html` — story creation
* `edit_story.html` — story editing
* `my_stories.html` — writer's story management
* `published_stories.html` — published story browsing
* `story_detail.html` — story information and reading options
* `create_chapter.html` — chapter creation
* `read_chapter.html` — chapter reading
* `reader_dashboard.html` — personalized reading dashboard
* `create_world.html` — world creation
* `world_explorer.html` — exploration of a story's fictional world
* `create_character.html` — character creation
* `add_character_image.html` — character image upload
* `create_location.html` — location creation
* `add_location_image.html` — location image upload
* `create_creature.html` — creature creation
* `add_creature_image.html` — creature image upload
* `add_world_image.html` — world image upload
* `create_timeline_event.html` — timeline event creation

### Backend

`views.py` contains the application's view functions for authentication, profiles, writer conversion, story management, publishing, chapters, reading, reading progress, reader dashboards, world-building, discovery, likes, comments, and other application functionality.

`models.py` contains the database models described above.

### Static Files

The static files contain the custom styling and JavaScript used throughout Loreverse.

`styles.css` contains custom styling for the navigation bar, story cards, Continue Reading cards, forms, buttons, typography, filtering interfaces, containers, responsive layouts, hover states, and other UI elements.

The `script.js` JavaScript files provide the application's interactive functionality, including theme switching, text-size controls, delete confirmation, and the World Explorer image viewer.

### Media

The `media/` directory contains uploaded images used by Loreverse, including story covers, profile pictures, world images, character images, location images, and creature images.

### Database

`db.sqlite3` contains the application's SQLite database and the populated sample content used to demonstrate Loreverse.

### Dependencies

`requirements.txt` contains the Python packages required by the project:

* Django
* Pillow

Pillow is used to support image fields and uploaded images throughout the application.

## How to Run

Make sure Python is installed on the computer.

Clone or download the project and open a terminal in the project's main directory.

It is recommended to create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

On Windows:

```bash
venv\Scripts\activate
```

On macOS/Linux:

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

Apply the Django database migrations:

```bash
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Then open the local Django server in a web browser, normally at:

```text
http://127.0.0.1:8000/
```

The project includes a populated SQLite database and the required `media/` directory so that the existing sample stories and uploaded images can be explored.

## Additional Information

Loreverse is designed so that a user does not need to choose between being exclusively a reader or exclusively a writer. Every registered user begins with Reader functionality, and a Reader can become a Writer when they want to create content. Becoming a Writer adds story and world-building capabilities while preserving the user's ability to read and manage their own reading collections.

The application also supports exploration without requiring every feature to be available to logged-out visitors. Logged-out users can view the public Loreverse interface, discover published stories, search content, and browse the available story listings, while authentication is required for personalized reading and account functionality.

The project uses Bootstrap together with custom CSS and JavaScript rather than relying entirely on default framework styling. The interface includes responsive story cards, cover images, Continue Reading sections, navigation controls, theme switching, loading behavior, image viewing, and other UI improvements intended to make the application feel like a complete reading and world-exploration platform.

The supplied `db.sqlite3` and `media/` directory are part of the project demonstration. They allow the application to be run with the sample Loreverse content already available rather than requiring the evaluator to create all content from an empty database.

Overall, Loreverse was built to demonstrate how Django models, authentication, relationships, templates, CSS, JavaScript, image handling, and responsive design can be combined to create a complete web application centered around both storytelling and exploration of fictional worlds
