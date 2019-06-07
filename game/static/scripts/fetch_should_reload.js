window.addEventListener('load', () => {

    requestsDelay = 2000;

    fetchIsMyTurn = () => {
        fetch(window._fetch_url)
            .then(res => res.json())
            .then(isMyTurn => {
                if(isMyTurn)
                    location.href = location.href;
                else
                    setTimeout(fetchIsMyTurn, requestsDelay);
            });
    }

    fetchIsMyTurn();

});