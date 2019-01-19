import React, { Component } from 'react';
import logo from './images/Stag Logo.png';
import './SyStagHeader.css';

class SyStagHeader extends Component {
  render() {
    return (
      <div className="jumbotron text-left">
        <div className='row'>
          <div className='col-sm-2'>
            <img src={logo} style={{height: 50+'%',	width: 50+'%'}}/>
          </div>
          <div className="col-sm-3">
            <h1>&nbsp;&nbsp;SyStag</h1>
          </div>
          <div className='col-sm-2 col-sm-offset-5'>
            <img src={logo} style={{height: 50+'%',	width: 50+'%'}}/>
          </div>
        </div>
      </div>

    );
  }
}

export default SyStagHeader;
