import '../css/aio.css'

export const Header = () =>{
    return <header>
        <nav>
            <span>Slurppass.</span>
            <ul>
                <li>Home</li>
                <li>Services</li>
                <li>About</li>
                <li>Contact</li>
            </ul>
            <a id='toppy'>Sign up/Log in</a>
        </nav>
    </header>
}

export const Footer = () => {
    return <footer>
        <p>this is a footer</p>
    </footer>
}

// export const Modal = () =>{
//     return <div>
//         <h3>Register</h3>
//     </div>
// }