# AuctionHousePricer

This is a simple Python program that connects to the Blizzard API and retrieves prices for certain commodities in the game World of Warcraft.

The SearchManager.py file includes the SearchManager class. It brings together all other classes and serves as the main service for the backend. It takes in as input a server name, and an item name, and returns a multitude of information on the item.

At the moment the backend only supports a specific in-game profession (Blacksmithing), but it'll eventually support all professions. Next steps include but are not limited to:

- Add error/success messages to each class;
- Create a proprietary database with professions details;
- Create front end and development server through Django;
- Host webservice on cloud (Google or Azure);
