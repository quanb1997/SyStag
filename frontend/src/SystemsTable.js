import React, { Component } from 'react';
import StateOfPage from './StateOfPage'
import './SystemsTable.css';
var i=0;
var id = "group-list-elem";
var id_sys = "systems-list-elem";


var x=0;
var tagsonsystem;

class SystemsTable extends Component {
  
  render() {
    return (
      <div className='container-fluid' id='main-div'>
      
        <div className='row'>
          <div className='col-sm-3' id='filter-div'>
            <div className='columns'>
              <div className="list-group">
              <li id = 'header' className="list-group-item active"><h3>Filters</h3></li>
                <ul>
                {this.props.filters.map(function(filtersValue){
                  return <a className="list-group-item" key={i++}>{filtersValue}</a>;
                })}

                </ul>

              </div>	
              <div className="list-group">
              <li id = 'header' className="list-group-item active"><h3>Tags</h3></li>
                <ul id="tag-ul">
                  <a className="list-group-item">Add Tag:
                    <input type="text" id="new-tag-name" placeholder="Enter New Tag Name"></input>
                    <button id="add-tag">
                      <span class="glyphicon glyphicon-plus">
                      </span>
                    </button>
                  </a>
                    {this.props.tags.map(function(tagValue){
                      return <a className="list-group-item" key={i++}>{tagValue}</a>;
                    })}

                </ul>

              </div>	
            </div>
          </div>
          <div className='col-sm-6' id='systems-div'>
            <div className='columns'>

              <div className="list-group" id="systems-list-group">
                <li id = 'header' className="list-group-item active"><h3>My Systems</h3></li>
                <ul>
                {this.props.list.map(function(listValue){
                  return <li className="list-group-item systems-list-elem"  key={x++}>{listValue[0]}
                  {/* tagsonsystem = StateOfPage.systemsAllInfo[x].tagnames
                  {this.props.tagsonsystem.map(function(tagname){
                    return 
                  })} */}
                  {/* {this.props.systemsinfo[x].map(function(val){<button type="button" class="btn btn-info" key={x++}>val.tagnames</button>})} */}
                  <span class="glyphicon glyphicon-remove rm"></span>
                  <span class="glyphicon glyphicon-info-sign info-span"></span>
                  <button type="button" class="btn btn-success" >Tag System</button>
                  <button type="button" class="btn btn-info" key={x++}>{listValue[1]}</button>

                  
                  </li>;
                })}

                </ul>

              </div>
            </div>
      
          </div>
      
          <div className='col-sm-3' id='groups-div'>
            <div className='columns'>
              
              <div className="list-group" id = "groups-list">
      
                <li id = 'header' className="list-group-item active group-list-elem"><h3>Groups</h3></li>
                {/* TODO change glyphicon to more intuitive    */}
                <ul>
                {this.props.groups.map(function(groupValue){
                  return <li className="list-group-item group-list-elem" key={i++} id={id}>{groupValue}</li>;
                })}

                </ul>

              </div>
            </div>
      
          </div>
      
        </div>
      </div>
    );
  }
}

export default SystemsTable;

  {/* <button type="button" className="btn btn-primary">
                      <span className="glyphicon glyphicon-sort-by-alphabet"></span>		
                    </button>
                    <button type="button" className="btn btn-primary">
                      <span className="glyphicon glyphicon-sort-by-alphabet-alt"></span>		
                    </button> */}