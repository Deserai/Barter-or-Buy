document.addEventListener('DOMContentLoaded', ()=>{
    const suggestions = document.getElementById('suggestions');
    suggestions.hidden = true;
    
    ['crop','crop2'].forEach(id => {
        const input = document.getElementById(id);
        if (!input){
            console.error('Could not find input element.');
            console.log('Available inputs:', document.querySelectorAll('input'));
            return;
        }
    
        if (!suggestions) {
            console.error('Could not find suggestions element with ID #suggestions');
            console.log('Available UL elements:', document.querySelectorAll('ul'));
            return;
        }

        document.getElementById(id)?.addEventListener('input', ()=>{
        const term = input.value.trim();
        if(term.length > 1){
            
            fetch(`${AUTOCOMPLETE_URL}?term=${encodeURIComponent(term)}`)
            .then(res =>res.json())
            .then(data=>{
                suggestions.hidden = false
                suggestions.innerHTML = '';
                data.forEach(item => {
                    const li = document.createElement('li'); 
                    li.textContent = item;
                    li.onclick =()=>{
                    input.value = item;
                    suggestions.innerHTML = '';
                    suggestions.hidden = true;
                    };
                    suggestions.appendChild(li);
                });
            });
            
        } else{
            suggestions.innerHTML = '';
        }
    });
});
});

   