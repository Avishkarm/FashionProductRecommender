import logo from './logo.png';
const Header = ({setSearchText}) =>{
    // const[searchText,setSearchText] = useState("");
    return(
        <div className="navbar-container"> 
            <img src={logo} alt="logo"/>
            <ul>
                <li>Navbar</li>
                <li>Home</li>
                <li>About us</li>
            </ul>
            <div className="search-container">
            <input type="textbox" 
            placeholder="Search here"
            // value={searchText}
            onChange={(e)=>
                {setSearchText(e.target.value);
            }}/>
            <button 
            className="search-btn"
            >Search</button>
            </div>
            
        </div>
    )
}

export default Header;