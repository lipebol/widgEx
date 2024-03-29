// Veja utilizando as linhas comentadas.

function async() {
    console.log('Começou!')
    //console.log('Aguardando...')
    fetch ('https://jsonplaceholder.typicode.com/posts')
    .then((response) => {
        if(response.status == 200) {
            return response.json()
        }
    })
    .then((json) => {
        console.log(json[0])
    })
    .then(() => {
        console.log('Terminou.')
    })    
    //console.log('Aguardando...')
    
}

async()