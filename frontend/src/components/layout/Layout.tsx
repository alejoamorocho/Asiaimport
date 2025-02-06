import { Outlet } from 'react-router-dom';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import Toast from '../common/Toast';
import Modal from '../common/Modal';
import { useSelector } from 'react-redux';
import { RootState } from '../../store';

const Layout = () => {
  const { toast, modal } = useSelector((state: RootState) => state.ui);

  return (
    <div className="min-h-screen bg-secondary-50">
      <Navbar />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-8">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
      {toast.show && <Toast />}
      {modal.show && <Modal />}
    </div>
  );
};

export default Layout;
