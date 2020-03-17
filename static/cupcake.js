async function wrapper(){
    const BASE_URL = "http://127.0.0.1:5000/api/cupcakes"

    cupcakeList = document.querySelector('#cupcake-list');

    create = document.querySelector('#create');
    flavor = document.querySelector('#flavor')
    size = document.querySelector('#size')
    rating = document.querySelector('#rating')
    image = document.querySelector('#image')

    filter = document.querySelector('#filter')
    search = document.querySelector('#search')


    class Cupcakes { 

        static async getCupcakes(){
            let response = await axios.get(BASE_URL);
            return response.data.cupcakes
        }

        static async submitFormCreated(evt){
            evt.preventDefault()
            let response = await axios.post(BASE_URL, this.params = {
                "flavor": flavor.value,
                "size": size.value,
                "rating": rating.value,
                "image": image.value
            });
            this.addCupcake(response.data.cupcake)
        
        }

        async submitFormSearch(evt){
            evt.preventDefault()
        
            let response = await axios.get(`${BASE_URL}/search/${search.value}`)
            
            if (response.data.cupcakes.length > 0) {
                while (cupcakeList.children.length > 0){
                    cupcakeList.firstElementChild.remove()
                }

                this.displayCupcakes(response.data.cupcakes)
            }
        }

        addCupcake(cupcakeObject){
            const LI = document.createElement('li');
            LI.setAttribute('data-id', cupcakeObject.id)
            LI.innerHTML = `${cupcakeObject.flavor} <span class='btn-sm btn-info'>X</span>`
            cupcakeList.append(LI)
        }

        displayCupcakes(array){
            for (let cake of array) {
                this.addCupcake(cake)
            }
        }

        async deleteCupcake(evt){
            if (evt.target.tagName === 'SPAN'){
                let response = await axios.delete(`${BASE_URL}/${evt.target.parentElement.getAttribute('data-id')}`)
                evt.target.parentElement.remove()
            }
        }


    }

    page = new Cupcakes()
    cupcakeList.addEventListener('click', page.deleteCupcake.bind(page) )
    create.addEventListener('submit', Cupcakes.submitFormCreated.bind(page));
    filter.addEventListener('submit', page.submitFormSearch.bind(page));

    //generate and display all cupcakes
    data = await Cupcakes.getCupcakes()
    page.displayCupcakes(data)
}

wrapper()

