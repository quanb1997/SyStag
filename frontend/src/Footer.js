import React, { Component } from 'react';
import './Footer.css'
class Footer extends Component{
	render(){
		return(
			<div className='container-fluid' id='footer'>
				<div className='row' id='top-footer-row'>
					<div className='col-sm-6'>
						<h4 id = "x">Tune Squad: Amherst, Massachusetts</h4>
						<p>Further Information</p>
						<p>Other Products</p>
					</div>
				</div>
			</div>
		);
	}
}

export default Footer;