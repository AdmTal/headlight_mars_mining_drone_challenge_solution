# Adam Tal's Headlight Mars Mining Drone Tournament Entry

Hi All,

This repo contains my solution to the 2018 NYC Headlight Mars Mining Drone Tournament.

My original submission is preserved in the .zip file.  The other files represent a few more hours of tinkering past the submission deadline.

Cheers,

Adam

# Instructions

1. First - clone the repository and enter the directory
    ```
    git clone https://github.com/AdmTal/headlight_mars_mining_drone_challenge_solution.git
    cd headlight_mars_mining_drone_challenge_solution
    ```
2. These two steps are optional -- to install dependencies into a virtualenv
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Run the setup script
    ```
    pip install -r requirements.txt
    ```

4. The Mars Mining Drone needs to communicate with a server - the server is available at it's original source : [https://github.com/HeadlightLabs/Tournament-API](https://github.com/HeadlightLabs/Tournament-API)

    If that is no longer available - I have it cloned it here : [https://github.com/AdmTal/Tournament-API](https://github.com/AdmTal/Tournament-API)

5. Once you have the server running
    ```
    bash start.sh
    ```

6. In order to run the bot - but also generate the image of the bot's path, run
    ```
    bash example_run_with_image.sh
    ```