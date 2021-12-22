<div id="top"></div>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<!--
<div align="center">
  <a href="https://github.com/chrisjackr/SugarWOD_Project">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
-->

<h3 align="center">SugarWOD Project</h3>

  <p align="center">
    SugarWOD webscraper - to collect, parse and save past CrossFit workouts.
    <!--
    <br />
    <a href="https://github.com/chrisjackr/SugarWOD_Project"><strong>Explore the docs »</strong></a>
    <br />
-->
    <br />
    <!--
    <a href="https://github.com/chrisjackr/SugarWOD_Project">View Demo</a>
    ·
    -->
    <a href="https://github.com/chrisjackr/SugarWOD_Project/issues">Report Bug</a>
    ·
    <a href="https://github.com/chrisjackr/SugarWOD_Project/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <!--<li><a href="#prerequisites">Prerequisites</a></li>-->
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <!--<li><a href="#roadmap">Roadmap</a></li>-->
    <!--<li><a href="#contributing">Contributing</a></li>-->
    <!--<li><a href="#license">License</a></li>-->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

<!--[![Product Name Screen Shot][product-screenshot]](https://example.com)-->

This project is a webscraper that collects previous CrossFit workouts from the SugarWOD website. Each workout has an associated date, title and workout description; each workout consists of different exercises (e.g. Deadlift) and workout types (e.g. AMRAP). These data are saved in a SQL databse so that workouts can be queried to find ones with a particular exercise etc. 

**WORK IN PROGRESS:**   
<strike>Interactive dashboard using <code>Bokeh</code> to display workout data.</strike>

**IMPROVEMENTS:**<br>
Please suggest future improvements <a href="https://github.com/chrisjackr/SugarWOD_Project/issues">here</a>!
<ul>
  <li><strike>SugarWOD may have an API available to use.</strike> Currently only available to gym owners.</li>
  <li>Use Splash + Docker to collect info from dynamically generated webpages.</li>
</ul>


<p align="right">(<a href="#top">back to top</a>)</p>





<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these steps:

<!--
### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* npm
  ```sh
  npm install npm@latest -g
  ```
-->

### Installation

1. Clone the repository to a suitable directory
   ```sh
   git clone https://github.com/chrisjackr/SugarWOD_Project.git
   ```
2. Create virtual environment and install packages from requirements.txt
   ```sh
   cd ../SugarWOD_Project
   py -m venv venv_name
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage
Once installed, scraping can begin by following these steps:
</br>
1. Update <code>credentials_template.py</code> template with <u>email</u>, <u>password</u> and <u>gym name</u> and save as <code>credentials.py</code>. If you have access to multiple gyms on the SugarWOD website, make sure the one you want to scrape is selected. Note, multiple gyms can be scraped and saved to different tables in the database file, but these will have to be run seperately.

2. To scrape workouts and save to a database, run the <code>main.py</code> in the ../SugarWOD directory. The choice to create a new database from scratch or append to an existing database is given as a **[Yes/No]** input (select **Y** if running for the first time. Choosing **N** in future will only add new workouts to the existing database - this would allow for old html files to be deleted.)

3. Once the database is updated, a dashboard .html file is generated. The option is given to shown this in a browser before script finishes.

The script will create a JSON file called **sugarwod_json_{gym_name}** and from this a database file called **sugarwod_sql.db**.
<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ROADMAP 
## Roadmap

- [] Feature 1
- [] Feature 2
- [] Feature 3
    - [] Nested Feature

See the [open issues](https://github.com/chrisjackr/SugarWOD_Project/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>
-->


<!-- CONTRIBUTING 
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>
-->


<!-- LICENSE 
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
-->


<!-- CONTACT -->
## Contact

Chris - chrisjackr

Project Link: [https://github.com/chrisjackr/SugarWOD_Project](https://github.com/chrisjackr/SugarWOD_Project)

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* []() Check out the <a href="https://www.sugarwod.com/">SugarWOD website</a>!


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/chrisjackr/SugarWOD_Project.svg?style=for-the-badge
[contributors-url]: https://github.com/chrisjackr/SugarWOD_Project/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/chrisjackr/SugarWOD_Project.svg?style=for-the-badge
[forks-url]: https://github.com/chrisjackr/SugarWOD_Project/network/members
[stars-shield]: https://img.shields.io/github/stars/chrisjackr/SugarWOD_Project.svg?style=for-the-badge
[stars-url]: https://github.com/chrisjackr/SugarWOD_Project/stargazers
[issues-shield]: https://img.shields.io/github/issues/chrisjackr/SugarWOD_Project.svg?style=for-the-badge
[issues-url]: https://github.com/chrisjackr/SugarWOD_Project/issues
[license-shield]: https://img.shields.io/github/license/chrisjackr/SugarWOD_Project.svg?style=for-the-badge
[license-url]: https://github.com/chrisjackr/SugarWOD_Project/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/chris-richardson-a42724195
[product-screenshot]: images/screenshot.png
