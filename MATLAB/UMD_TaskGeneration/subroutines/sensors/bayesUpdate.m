function [V, U, O] = bayesUpdate( cellDetMat , V, U, O, cellsInView, mapSignals, targSignals, g_V, g_UO, z_VU, z_O )

for i = 1:1:size(cellsInView,1)
    bx = cellsInView(i,1);
    by = cellsInView(i,2);
    if ( cellDetMat(by,bx) == 0 )
        l = mapSignals(i);
        q = targSignals(i);
        p_g_z = V(by,bx)*g_V(l)*z_VU(q) + U(by,bx)*g_UO(l)*z_VU(q) + O(by,bx)*g_UO(l)*z_O(q);
        V(by,bx) = V(by,bx)*g_V(l)*z_VU(q)/p_g_z;
        U(by,bx) = U(by,bx)*g_UO(l)*z_VU(q)/p_g_z;
        O(by,bx) = O(by,bx)*g_UO(l)*z_O(q)/p_g_z;
        
%         figure(100);
%         subplot(2,2,1)
%         imagesc(V); caxis([0 1])
%         subplot(2,2,2)
%         imagesc(U); caxis([0 1])
%         subplot(2,2,3)
%         imagesc(O); caxis([0 1])
%         subplot(2,2,4)
%         imagesc(O./U);
%         colorbar;
%         title('Initial')
%         disp('----')
%         by
%         bx
%         i
%         l
%         q
    end
end