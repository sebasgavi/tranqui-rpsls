window.addEventListener('load', () => {

    requestsDelay = 2000;

    fetchShouldEnterGame = () => {
        fetch(window._fetch_url)
            .then(res => res.text())
            .then(url => {
                if(url)
                    location.href = url;
                else
                    setTimeout(fetchShouldEnterGame, requestsDelay);
            });
    }

    fetchShouldEnterGame();

});