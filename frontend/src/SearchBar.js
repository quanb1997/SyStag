import React, { Component } from 'react';
import './SearchBar.css';

class SearchBar extends Component {
  
  render() {
        return (
            <div class='container-fluid' id='search-div'>
                <div class='row' style={{padding: 0}}>
                    <div class='col-sm-2 col-sm-offset-1'>
                        {/* <button onclick="">Advanced Search<span class="glyphicon glyphicon-search"></span></button> */}
                    </div>
                    
                    <div class='col-sm-4'   >
                            <input onclick="javascript::searchSystems()" value='Quick Search' type="submit" id="submit-search"></input>
                            <input type="search" id='searchbar'></input>
                    </div>
                    
                    <div class='col-sm-1'>
                        <button onclick="">Logout<span class="glyphicon glyphicon-log-out"></span></button>
                    </div>
                </div>
            </div>

        );
    }
}

export default SearchBar;