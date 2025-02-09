import React from 'react';
import { Box, Container, Flex } from '@chakra-ui/react';
import { Navbar } from '../components/Navbar';
import { Sidebar } from '../components/Sidebar';
import { useAuth } from '../../features/auth/hooks/useAuth';

interface MainLayoutProps {
  children: React.ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Box>{children}</Box>;
  }

  return (
    <Flex minH="100vh">
      <Sidebar />
      <Box flex="1">
        <Navbar />
        <Container maxW="container.xl" py={8}>
          {children}
        </Container>
      </Box>
    </Flex>
  );
}
